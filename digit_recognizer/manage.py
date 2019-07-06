from stairs import StairsProject
from stairs.services.management import init_cli

if __name__ == "__main__":
    StairsProject('config.py')
    init_cli()
