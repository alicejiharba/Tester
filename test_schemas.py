import importlib
import inspect
import pytest
from pydantic import BaseModel

# list of schema modules to test (adjust if you add/remove schema modules)
MODULES = [
    "app.schemas.space",
    "app.schemas.booking",
    "app.schemas.user",
    "app.schemas.utility",
    "app.schemas.rating",
    "app.schemas.penalty",
    "app.schemas.auth",
]


def _construct_model_without_validation(cls):
    """
    Construct a model instance without running full validation.
    Works with both pydantic v1 (.construct) and v2 (.model_construct).
    """
    if hasattr(cls, "model_construct"):
        return cls.model_construct()
    if hasattr(cls, "construct"):
        return cls.construct()
    pytest.skip(f"Cannot construct instance for {cls.__name__}")


def test_schema_modules_have_pydantic_models():
    for mod_name in MODULES:
        mod = importlib.import_module(mod_name)
        models = [
            obj
            for _, obj in inspect.getmembers(mod, inspect.isclass)
            if issubclass(obj, BaseModel) and obj.__module__ == mod.__name__
        ]
        assert models, f"No Pydantic models found in module {mod_name}"
        for cls in models:
            # ensure the class exposes either new pydantic v2 config or the legacy Config
            assert hasattr(cls, "model_config") or hasattr(cls, "Config"), (
                f"{cls.__name__} in {mod_name} lacks model_config (v2) and Config (v1)"
            )
            # ensure we can create an instance without providing field data (no validation)
            inst = _construct_model_without_validation(cls)
            assert isinstance(inst, BaseModel)


def test_schema_models_have_readable_fields():
    for mod_name in MODULES:
        mod = importlib.import_module(mod_name)
        models = [
            obj
            for _, obj in inspect.getmembers(mod, inspect.isclass)
            if issubclass(obj, BaseModel) and obj.__module__ == mod.__name__
        ]
        for cls in models:
            # ensure the model exposes some field metadata (fields may be empty but attribute must exist)
            try:
                has_fields_v2 = hasattr(cls, "model_fields")
                has_fields_v1 = hasattr(cls, "__fields__")
                assert has_fields_v2 or has_fields_v1
            except Exception as e:
                pytest.fail(f"Unable to introspect fields of {cls.__name__} in {mod_name}: {e}")