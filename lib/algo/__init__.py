import pathlib
import importlib

def list_algos():
    return __files

def rescan_algos():
    __files = list({x.name.rsplit('.', 1)[0] for x in __thisdir.glob("*.py") if x.name != __thisfile.name})
    return __files

def load_mod(name):
    return importlib.import_module('..'+name, 'lib.algo.subpkg')

__thisfile = pathlib.Path(__file__)
__thisdir = pathlib.Path(__file__).parent.resolve()
__files = rescan_algos()
# __all__ = __files + [list_algos, rescan_algos]