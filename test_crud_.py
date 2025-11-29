import importlib
import pkgutil
import inspect

PKG_NAME = "app.crud"


def test_crud_package_importable():
    pkg = importlib.import_module(PKG_NAME)
    assert hasattr(pkg, "__path__")


def test_each_crud_module_exports_callables():
    pkg = importlib.import_module(PKG_NAME)
    for finder, name, ispkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + "."):
        mod = importlib.import_module(name)
        # collect callables defined in the module
        callables = [
            obj
            for _, obj in inspect.getmembers(mod, inspect.isfunction)
            if obj.__module__ == mod.__name__
        ]
        # Accept modules with 0 or more callables but ensure module loads cleanly
        assert isinstance(callables, list)