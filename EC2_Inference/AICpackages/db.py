import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv("/home/ubuntu/AIC_Inference/.credentials")

class Database_X:
    def __init__(self, 
                 host=os.getenv("ENDPOINT"), 
                 port=os.getenv("PORT"),
                 user=os.getenv("USERNAME"),
                 passwd=os.getenv("PASSWORD"),
                 database=os.getenv("DB")):
        self.host, self.port, self.user, self.passwd, self.database = host, port, user, passwd, database

        self.conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.passwd,
            database=self.database
        )

        self.cursor = self.conn.cursor()
    
    def tel_update(self, origin):
        sql = "SELECT emergency_counter FROM dashboard_cameras WHERE kinesis_datastream_name = %s"
        val = (origin,)

        self.cursor.execute(sql, val)
        emergency_counter = int(self.cursor.fetchone()[0])
        emergency_counter+=1

        sql = "UPDATE dashboard_cameras SET emergency_counter = %s WHERE kinesis_datastream_name = %s"
        val = (emergency_counter, origin)

        self.cursor.execute(sql, val)
        self.conn.commit()

    def acc_update(self, origin):
        sql = "SELECT accidents_total_counter FROM dashboard_cameras WHERE kinesis_datastream_name = %s"
        val = (origin,)

        self.cursor.execute(sql, val)
        accidents_total_counter = int(self.cursor.fetchone()[0])
        accidents_total_counter+=1

        sql = "UPDATE dashboard_cameras SET accidents_total_counter = %s WHERE kinesis_datastream_name = %s"
        val = (accidents_total_counter, origin)

        self.cursor.execute(sql, val)
        self.conn.commit()

    def vech_update(self, origin):
        sql = "SELECT vehicle_counter FROM dashboard_cameras WHERE kinesis_datastream_name = %s"
        val = (origin,)

        self.cursor.execute(sql, val)
        vehicle_counter = int(self.cursor.fetchone()[0])
        vehicle_counter+=1

        sql = "UPDATE dashboard_cameras SET vehicle_counter = %s WHERE kinesis_datastream_name = %s"
        val = (vehicle_counter, origin)

        self.cursor.execute(sql, val)
        self.conn.commit()
    
    def close(self):
        self.cursor.close()
        self.conn.close()