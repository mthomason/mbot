# -*- coding: utf-8 -*-

from enum import Enum

class DatabaseType(Enum):
	SQLITE = "sqlite"
	MYSQL = "mysql"
	MSSQL = "mssql"
	ODBC = "odbc"
	
