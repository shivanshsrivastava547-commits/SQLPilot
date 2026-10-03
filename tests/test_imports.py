import importlib


def test_project_modules_import():
    modules = [
        "config",
        "app",
        "agent",
        "database",
        "tools",
        "analysis",
        "visualization",
        "models",
        "ui",
    ]

    for module_name in modules:
        importlib.import_module(module_name)
