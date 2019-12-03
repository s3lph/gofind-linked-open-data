
import mysql.connector as mysql

from untitled_project.database.schema import BaseSchema


class Transaction:

    def __init__(self, db: mysql.MySQLConnection, consistent_snapshot=False, isolation=None, readonly=None):
        self._db = db
        self._snapshot = consistent_snapshot
        self._isolation = isolation
        self._ro = readonly

    def __enter__(self):
        self._db.start_transaction(consistent_snapshot=self._snapshot,
                                   isolation_level=self._isolation,
                                   readonly=self._ro)
        return self._db.cursor(prepared=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self._db.rollback()
        else:
            self._db.commit()


class DatabaseConnection:

    __SCHEMA_TABLE = '_SCHEMA_VERSION_'

    def __init__(self,
                 host: str = 'localhost',
                 port: int = 3306,
                 database: str = None,
                 user: str = None,
                 password: str = None):
        self._con = mysql.connect(host=host, port=port,
                                  database=database, user=user, password=password,
                                  charset='utf8mb4', collation='utf8mb4_unicode_ci')
        self.create_schema()

    def transaction(self, consistent_snapshot=False, isolation=None, readonly=None):
        return Transaction(self._con, consistent_snapshot, isolation, readonly)

    def create_schema(self):
        # Make sure the schema version table exists and is primed with 0
        with self.transaction(consistent_snapshot=True, isolation='SERIALIZABLE') as c:
            c.execute('SHOW TABLES')
            tables = [r[0] for r in c.fetchall()]
            if DatabaseConnection.__SCHEMA_TABLE not in tables:
                c.execute(f"""
                    CREATE TABLE {DatabaseConnection.__SCHEMA_TABLE} (
                        version INTEGER,
                        minor INTEGER
                    )
                """)
                c.execute(f'INSERT INTO {DatabaseConnection.__SCHEMA_TABLE} VALUES (0, 0)')

        with self.transaction(consistent_snapshot=True, isolation='SERIALIZABLE') as c:
            # Fetch the schema version
            c.execute(f'SELECT version, minor FROM {DatabaseConnection.__SCHEMA_TABLE} LIMIT 1')
            row = c.fetchone()
        if not row:
            row = 0, 0
        version, minor = row
        # Apply one single migration after the other until the latest version is reached
        target = BaseSchema.latest()
        for migration, major, minor in BaseSchema.migrate(version, minor, to=target.version()):
            with self.transaction(consistent_snapshot=True, isolation='SERIALIZABLE') as c:
                c.execute(migration)
                c.execute(f'UPDATE {DatabaseConnection.__SCHEMA_TABLE} SET version = %s, minor = %s',
                          (major, minor))


if __name__ == '__main__':
    DatabaseConnection(database='foo', user='foo', password='bar')
