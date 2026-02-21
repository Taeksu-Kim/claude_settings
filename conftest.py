import pytest
import importlib.util
import importlib.machinery
import sys


def pytest_collect_file(parent, file_path):
    if file_path.suffix == ".test" and ".py." in file_path.name:
        return PyTestFile.from_parent(parent, path=file_path)


class PyTestFile(pytest.Module):
    def _getobj(self):
        module_name = f"_test_{self.path.stem.replace('.', '_')}"
        loader = importlib.machinery.SourceFileLoader(module_name, str(self.path))
        spec = importlib.util.spec_from_loader(module_name, loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
