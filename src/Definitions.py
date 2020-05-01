import pathlib

PATH_ROOT = pathlib.Path(__file__).parent.parent.absolute()
PATH_SRC = pathlib.Path(__file__).parent.absolute()
PATH_RES = PATH_ROOT.joinpath("res").absolute()
