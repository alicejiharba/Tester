import importlib
import pkgutil
import inspect

PKG_NAME = "app.models"


def test_models_package_importable():
    pkg = importlib.import_module(PKG_NAME)
    assert hasattr(pkg, "__path__")


def test_model_modules_define_tablenames():
    pkg = importlib.import_module(PKG_NAME)
    found = []
    for finder, name, ispkg in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + "."):
        mod = importlib.import_module(name)
        classes = [
            obj
            for _, obj in inspect.getmembers(mod, inspect.isclass)
            if obj.__module__ == mod.__name__
        ]
        for cls in classes:
            if hasattr(cls, "__tablename__"):
                found.append((name, cls.__name__))
    # Ensure at least one model class with __tablename__ exists
    assert found, "No ORM models with __tablename__ found in app.models package"