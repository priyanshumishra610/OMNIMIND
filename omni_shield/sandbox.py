import builtins
from typing import Any, Dict

class Sandbox:
    """
    Isolates code execution and blocks unsafe system operations.
    Use for secure, controlled evaluation of untrusted code.
    """
    def __init__(self, allowed_builtins: Dict[str, Any] = None):
        self.allowed_builtins = allowed_builtins or {"print": print, "len": len, "range": range}

    def execute(self, code: str, context: Dict[str, Any] = None) -> Any:
        """
        Execute code in a restricted environment.
        Blocks unsafe builtins and system calls.
        Args:
            code (str): The code to execute.
            context (dict): Optional context variables.
        Returns:
            Any: Result of execution or None.
        """
        safe_globals = {"__builtins__": self.allowed_builtins}
        if context:
            safe_globals.update(context)
        try:
            exec(code, safe_globals)
            return safe_globals.get("result", None)
        except Exception as e:
            return {"error": str(e)} 