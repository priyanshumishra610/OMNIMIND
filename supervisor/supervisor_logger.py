"""
Supervisor Logging System
Provides structured logging capabilities for the supervisor components.
"""

import os
import json
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, Union
from pathlib import Path
from logging.handlers import RotatingFileHandler
import threading


class SupervisorLogger:
    """
    Enhanced logging system for supervisor components with structured output,
    multiple handlers, and context-aware logging.
    """
    
    def __init__(self, 
                 log_dir: str = "logs",
                 log_level: str = "INFO",
                 max_file_size: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5,
                 structured_format: bool = True):
        """
        Initialize the supervisor logger.
        
        Args:
            log_dir: Directory to store log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            max_file_size: Maximum size of log file before rotation
            backup_count: Number of backup log files to keep
            structured_format: Whether to use structured JSON logging
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.structured_format = structured_format
        self._lock = threading.Lock()
        
        # Create main logger
        self.logger = logging.getLogger("supervisor")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Setup file handler with rotation
        log_file = self.log_dir / "supervisor.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        
        # Setup console handler
        console_handler = logging.StreamHandler()
        
        # Setup formatters
        if structured_format:
            formatter = StructuredFormatter()
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Component-specific loggers
        self._component_loggers = {}
        
        # Log context stack for contextual logging
        self._context_stack = threading.local()
        
        # Initialize metrics
        self.metrics = LogMetrics()
    
    def get_component_logger(self, component_name: str) -> logging.Logger:
        """Get or create a logger for a specific component."""
        if component_name not in self._component_loggers:
            component_logger = logging.getLogger(f"supervisor.{component_name}")
            component_logger.setLevel(self.logger.level)
            
            # Use same handlers as main logger
            for handler in self.logger.handlers:
                component_logger.addHandler(handler)
            
            self._component_loggers[component_name] = component_logger
        
        return self._component_loggers[component_name]
    
    def push_context(self, **context):
        """Push logging context onto the stack."""
        if not hasattr(self._context_stack, 'contexts'):
            self._context_stack.contexts = []
        
        self._context_stack.contexts.append(context)
    
    def pop_context(self):
        """Pop the most recent context from the stack."""
        if hasattr(self._context_stack, 'contexts') and self._context_stack.contexts:
            return self._context_stack.contexts.pop()
        return {}
    
    def get_current_context(self) -> Dict[str, Any]:
        """Get the merged context from the stack."""
        if not hasattr(self._context_stack, 'contexts'):
            return {}
        
        context = {}
        for ctx in self._context_stack.contexts:
            context.update(ctx)
        return context
    
    def _format_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format a log message with context."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "thread_id": threading.get_ident(),
        }
        
        # Add current context
        current_context = self.get_current_context()
        if current_context:
            log_entry["context"] = current_context
        
        # Add additional context
        if context:
            if "context" in log_entry:
                log_entry["context"].update(context)
            else:
                log_entry["context"] = context
        
        return log_entry
    
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None, component: str = None):
        """Log debug message."""
        with self._lock:
            self.metrics.increment_count("debug")
            logger = self.get_component_logger(component) if component else self.logger
            
            if self.structured_format:
                log_data = self._format_message(message, context)
                logger.debug(json.dumps(log_data))
            else:
                logger.debug(f"{message} {context or ''}")
    
    def info(self, message: str, context: Optional[Dict[str, Any]] = None, component: str = None):
        """Log info message."""
        with self._lock:
            self.metrics.increment_count("info")
            logger = self.get_component_logger(component) if component else self.logger
            
            if self.structured_format:
                log_data = self._format_message(message, context)
                logger.info(json.dumps(log_data))
            else:
                logger.info(f"{message} {context or ''}")
    
    def warning(self, message: str, context: Optional[Dict[str, Any]] = None, component: str = None):
        """Log warning message."""
        with self._lock:
            self.metrics.increment_count("warning")
            logger = self.get_component_logger(component) if component else self.logger
            
            if self.structured_format:
                log_data = self._format_message(message, context)
                logger.warning(json.dumps(log_data))
            else:
                logger.warning(f"{message} {context or ''}")
    
    def error(self, message: str, exception: Optional[Exception] = None, 
              context: Optional[Dict[str, Any]] = None, component: str = None):
        """Log error message with optional exception details."""
        with self._lock:
            self.metrics.increment_count("error")
            logger = self.get_component_logger(component) if component else self.logger
            
            error_context = context or {}
            
            if exception:
                error_context.update({
                    "exception_type": type(exception).__name__,
                    "exception_message": str(exception),
                    "traceback": traceback.format_exc()
                })
            
            if self.structured_format:
                log_data = self._format_message(message, error_context)
                logger.error(json.dumps(log_data))
            else:
                logger.error(f"{message} {error_context}")
    
    def critical(self, message: str, exception: Optional[Exception] = None,
                 context: Optional[Dict[str, Any]] = None, component: str = None):
        """Log critical message."""
        with self._lock:
            self.metrics.increment_count("critical")
            logger = self.get_component_logger(component) if component else self.logger
            
            error_context = context or {}
            
            if exception:
                error_context.update({
                    "exception_type": type(exception).__name__,
                    "exception_message": str(exception),
                    "traceback": traceback.format_exc()
                })
            
            if self.structured_format:
                log_data = self._format_message(message, error_context)
                logger.critical(json.dumps(log_data))
            else:
                logger.critical(f"{message} {error_context}")
    
    def log_task_event(self, task_id: str, event: str, details: Optional[Dict[str, Any]] = None):
        """Log task-specific events."""
        context = {
            "task_id": task_id,
            "event_type": "task_event",
            "event": event
        }
        
        if details:
            context.update(details)
        
        self.info(f"Task {event}: {task_id}", context, component="task_manager")
    
    def log_component_event(self, component: str, event: str, details: Optional[Dict[str, Any]] = None):
        """Log component-specific events."""
        context = {
            "component": component,
            "event_type": "component_event",
            "event": event
        }
        
        if details:
            context.update(details)
        
        self.info(f"Component {event}: {component}", context, component=component)
    
    def log_performance_metric(self, metric_name: str, value: float, unit: str = "ms",
                              context: Optional[Dict[str, Any]] = None):
        """Log performance metrics."""
        perf_context = {
            "metric_type": "performance",
            "metric_name": metric_name,
            "value": value,
            "unit": unit
        }
        
        if context:
            perf_context.update(context)
        
        self.info(f"Performance metric: {metric_name}={value}{unit}", perf_context)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get logging metrics."""
        return self.metrics.get_all_metrics()
    
    def set_level(self, level: str):
        """Change logging level."""
        self.logger.setLevel(getattr(logging, level.upper()))
        for component_logger in self._component_loggers.values():
            component_logger.setLevel(getattr(logging, level.upper()))
    
    def flush(self):
        """Flush all handlers."""
        for handler in self.logger.handlers:
            handler.flush()


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging."""
    
    def format(self, record):
        # If the message is already JSON, use it as-is
        try:
            json.loads(record.getMessage())
            return record.getMessage()
        except (json.JSONDecodeError, ValueError):
            # Otherwise, create structured format
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "thread_id": record.thread,
                "process_id": record.process
            }
            
            if record.exc_info:
                log_entry["exception"] = self.formatException(record.exc_info)
            
            return json.dumps(log_entry)


class LogMetrics:
    """Tracks logging metrics and statistics."""
    
    def __init__(self):
        self._metrics = {
            "debug": 0,
            "info": 0,
            "warning": 0,
            "error": 0,
            "critical": 0
        }
        self._start_time = datetime.utcnow()
        self._lock = threading.Lock()
    
    def increment_count(self, level: str):
        """Increment counter for log level."""
        with self._lock:
            if level in self._metrics:
                self._metrics[level] += 1
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        with self._lock:
            uptime = (datetime.utcnow() - self._start_time).total_seconds()
            total_logs = sum(self._metrics.values())
            
            return {
                "counts": self._metrics.copy(),
                "total_logs": total_logs,
                "uptime_seconds": uptime,
                "logs_per_second": total_logs / uptime if uptime > 0 else 0,
                "start_time": self._start_time.isoformat()
            }


class LogContext:
    """Context manager for temporary logging context."""
    
    def __init__(self, logger: SupervisorLogger, **context):
        self.logger = logger
        self.context = context
    
    def __enter__(self):
        self.logger.push_context(**self.context)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.pop_context()


class ComponentLogger:
    """Specialized logger for supervisor components."""
    
    def __init__(self, supervisor_logger: SupervisorLogger, component_name: str):
        self.supervisor_logger = supervisor_logger
        self.component_name = component_name
        self.logger = supervisor_logger.get_component_logger(component_name)
    
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.supervisor_logger.debug(message, context, self.component_name)
    
    def info(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.supervisor_logger.info(message, context, self.component_name)
    
    def warning(self, message: str, context: Optional[Dict[str, Any]] = None):
        self.supervisor_logger.warning(message, context, self.component_name)
    
    def error(self, message: str, exception: Optional[Exception] = None, 
              context: Optional[Dict[str, Any]] = None):
        self.supervisor_logger.error(message, exception, context, self.component_name)
    
    def critical(self, message: str, exception: Optional[Exception] = None,
                 context: Optional[Dict[str, Any]] = None):
        self.supervisor_logger.critical(message, exception, context, self.component_name)
    
    def log_event(self, event: str, details: Optional[Dict[str, Any]] = None):
        """Log component-specific event."""
        self.supervisor_logger.log_component_event(self.component_name, event, details)
    
    def with_context(self, **context):
        """Return a context manager with additional context."""
        return LogContext(self.supervisor_logger, component=self.component_name, **context)


# Convenience functions for global logger instance
_global_logger: Optional[SupervisorLogger] = None


def get_logger() -> SupervisorLogger:
    """Get or create the global supervisor logger."""
    global _global_logger
    if _global_logger is None:
        _global_logger = SupervisorLogger()
    return _global_logger


def get_component_logger(component_name: str) -> ComponentLogger:
    """Get a component-specific logger."""
    return ComponentLogger(get_logger(), component_name)


def setup_logging(log_dir: str = "logs", log_level: str = "INFO", 
                  structured_format: bool = True) -> SupervisorLogger:
    """Setup global logging configuration."""
    global _global_logger
    _global_logger = SupervisorLogger(
        log_dir=log_dir,
        log_level=log_level,
        structured_format=structured_format
    )
    return _global_logger


# Example usage and testing
if __name__ == "__main__":
    # Setup logging
    logger = setup_logging(log_dir="test_logs", log_level="DEBUG")
    
    # Basic logging
    logger.info("Supervisor system starting", {"version": "1.0.0"})
    logger.debug("Debug information", {"debug_flag": True})
    logger.warning("This is a warning", {"alert_level": "medium"})
    
    # Component logging
    task_logger = get_component_logger("task_manager")
    task_logger.info("Task manager initialized")
    task_logger.log_event("startup", {"tasks_loaded": 5})
    
    # Context logging
    with task_logger.with_context(task_id="task_123"):
        task_logger.info("Processing task")
        task_logger.debug("Task details", {"priority": "high"})
    
    # Error logging
    try:
        raise ValueError("Test exception")
    except Exception as e:
        logger.error("An error occurred", exception=e, context={"operation": "test"})
    
    # Performance logging
    logger.log_performance_metric("task_processing_time", 150.5, "ms", 
                                 {"task_type": "analysis"})
    
    # Task events
    logger.log_task_event("task_456", "started", {"priority": "high", "agent": "worker_1"})
    logger.log_task_event("task_456", "completed", {"duration": 2.5, "result": "success"})
    
    # Get metrics
    metrics = logger.get_metrics()
    print(f"Logging metrics: {json.dumps(metrics, indent=2)}")
    
    # Flush logs
    logger.flush()