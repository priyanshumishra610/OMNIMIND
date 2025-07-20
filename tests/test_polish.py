from polish.performance_tuner import PerformanceTuner
from polish.config_validator import ConfigValidator
from polish.dependency_checker import DependencyChecker
from polish.doc_generator import DocGenerator
import types

def test_performance_tuner():
    """Test PerformanceTuner benchmarks latency."""
    pt = PerformanceTuner()
    def dummy(): return 42
    result = pt.benchmark(dummy)
    assert result["result"] == 42
    assert result["latency"] >= 0

def test_config_validator():
    """Test ConfigValidator validates .env and runtime (stub)."""
    cv = ConfigValidator(env_path=".env")
    valid = cv.validate_env()
    assert isinstance(valid, bool)
    valid_runtime = cv.validate_runtime({"foo": "bar"})
    assert valid_runtime

def test_dependency_checker():
    """Test DependencyChecker checks dependencies (stub)."""
    dc = DependencyChecker()
    result = dc.check()
    assert "missing" in result and "mismatched" in result

def test_doc_generator():
    """Test DocGenerator builds docs from docstrings (stub)."""
    def foo():
        """Foo docstring."""
        pass
    mod = types.ModuleType("mod")
    mod.foo = foo
    dg = DocGenerator()
    docs = dg.generate_for_module(mod)
    assert "foo" in docs and "Foo docstring." in docs["foo"] 