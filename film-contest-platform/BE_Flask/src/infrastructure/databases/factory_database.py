import os
from src.infrastructure.databases.abstract_database import AbstractDatabase
from src.infrastructure.databases.database_postgres import DatabasePostgres
from src.infrastructure.databases.database_mysql import DatabaseMySQL
from src.infrastructure.databases.database_mssql import DatabaseMSSQL

class FactoryDatabase:
    """
    Factory Pattern quản lý việc khởi tạo kết nối cơ sở dữ liệu.
    Cho phép chuyển đổi linh hoạt giữa PostgreSQL, MySQL và MS SQL Server
    chỉ bằng cách thay đổi giá trị biến môi trường DB_TYPE trong file .env.
    """
    @staticmethod
    def get_database(database_type: str = None) -> AbstractDatabase:
        if not database_type:
            database_type = os.environ.get('DB_TYPE', 'POSTGREE').upper()

        if database_type in ('POSTGREE', 'POSTGRES', 'POSTGRESQL'):
            return DatabasePostgres()
        elif database_type == 'MYSQL':
            return DatabaseMySQL()
        elif database_type in ('MSSQL', 'SQLSERVER'):
            return DatabaseMSSQL()
        raise ValueError(f"Hệ quản trị CSDL không được hỗ trợ: {database_type}")
