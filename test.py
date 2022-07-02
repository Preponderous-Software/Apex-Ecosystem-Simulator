from py_env_lib.src.main.python.preponderous.py_env_lib.entity import Entity
from py_env_lib.src.main.python.preponderous.py_env_lib.environment import Environment

# TODO: fix imports

entity = Entity()
environment = Environment()
environment.addEntity(entity)

environment.printInfo()