import pathlib

__thisdir = pathlib.Path(__file__).parent.resolve()
__all__ = [x.name for x in __thisdir.glob("*.py") if x.name != __file__]