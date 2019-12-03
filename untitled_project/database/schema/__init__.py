import importlib
import os

from untitled_project.database.schema.base import BaseSchema


# Import all schema definitions automatically
for file in os.listdir(os.path.join(os.path.dirname(__file__), 'schemas')):
    if file.endswith('.py'):
        importlib.import_module(f'untitled_project.database.schema.schemas.{file[:-3]}')
