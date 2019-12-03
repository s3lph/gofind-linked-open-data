
from typing import List, Tuple, Type

import abc


class BaseSchema(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def version() -> int:
        pass

    @classmethod
    def minor(cls) -> int:
        return len(cls.migrations())

    @staticmethod
    def migrate(from_major: int, from_minor: int, to: int) -> List[Tuple[str, int, int]]:
        migrations = []
        schemas: List[Type[BaseSchema]] = \
            sorted([s for s in BaseSchema.__subclasses__() if from_major <= s.version() <= to],
                   key=lambda t: t.version())
        for schema in schemas:
            major = schema.version()
            for minor, migration in enumerate(schema.migrations(), start=1):
                if from_major < major <= to:
                    migrations.append((migration, major, minor))
                elif major == from_major and minor > from_minor:
                    migrations.append((migration, major, minor))
        return migrations

    @staticmethod
    @abc.abstractmethod
    def migrations() -> List[str]:
        pass

    @staticmethod
    def latest() -> Type['BaseSchema']:
        return max(BaseSchema.__subclasses__(), key=lambda t: t.version())
