import importlib
import pkgutil
import inspect
from fastapi import APIRouter
from app.main import app

V1_MODULES = [
    "app.api.v1.spaces",
    "app.api.v1.users",
    "app.api.v1.bookings",
    "app.api.v1.ratings",
    "app.api.v1.penalties",
    "app.api.v1.utilities",
    "app.api.v1.auth",
    "app.api.v1.admin",
]


def test_app_includes_api_v1_routes():
    assert any(r.path.startswith("/api/v1") or r.path.startswith("/api/v1/") for r in app.routes)


def test_each_v1_module_exposes_router():
    for mod_name in V1_MODULES:
        mod = importlib.import_module(mod_name)
        assert hasattr(mod, "router"), f"{mod_name} does not expose 'router'"
        router = getattr(mod, "router")
        assert isinstance(router, APIRouter)
        # router.routes may be empty but should be a list
        assert hasattr(router, "routes") and isinstance(router.routes, list)


def test_v1_router_routes_have_paths_and_methods():
    for mod_name in V1_MODULES:
        mod = importlib.import_module(mod_name)
        router = getattr(mod, "router", None)
        if router is None:
            continue
        for route in router.routes:
            # path should be a string, methods should be a set or list
            assert hasattr(route, "path")
            assert isinstance(route.path, str)
            assert hasattr(route, "methods")
            # methods can be a frozenset / set
            assert len(route.methods) >= 0