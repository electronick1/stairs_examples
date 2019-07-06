import pickle

from stairs import StairsProject
from stairs.services.management import init_cli

if __name__ == "__main__":
    StairsProject('config.py', data_pickeler=pickle)
    init_cli()
