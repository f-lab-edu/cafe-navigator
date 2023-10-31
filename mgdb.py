import os 
from datetime import datetime
import logging
import pymysql

class MysqlManager:
    def __init__(self) -> None:
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        db_name = os.getenv("DB_NAME")
        self.conn = pymysql.connect(user=user, password=password, host=host, port=3306, db=db_name, charset='utf8')

    def insert_cafe(self, documents) -> None:
        logging.info("insert mgdb start")
        val = []
        cursor = self.conn.cursor()
        now = datetime.now()
        sql = "INSERT INTO cafe (name, latitude, longitude, created_by, created_at, modified_at) \
            VALUES (%s, %s, %s, %s, %s, %s)"
        for cafe in documents:
            val.append((cafe['place_name'], cafe['y'], cafe['x'], 0, now, now))
        print(val)
        cursor.executemany(sql, val)
        self.conn.commit()
        logging.info(f"insert {cursor.rowcount} cafes")
            
    def close(self) -> None:
        logging.info("mgdb connection closed")
        self.conn.close()