"""Load a skill's tool by path, so tests work without packages or sys.path tricks."""
import importlib.util
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def load_tool(skill, module):
    path = os.path.join(ROOT, "skills", skill, "scripts", module + ".py")
    spec = importlib.util.spec_from_file_location("%s_%s" % (skill.replace("-", "_"), module), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
