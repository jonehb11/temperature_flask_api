import os
import psycopg2
from flask import Flask,request
from dotenv import load_dotenv


CREATE_ROOMS_TABLE = (
    "CREATE TABLE IF NOT EXISTS rooms(id SERIAL PRIMARY KEY, name TEXT);"
)
CREATE_TEMPS_TABLE = (
    """"CREATE TABLE IF NOT EXISTS temperatures(room_id INTEGER, temperature REAL, date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"""

)
INSERT_ROOM_RETURN_ID = "INSERT INTO rooms(name)VALUES(%s) RETURNING id;"
INSERT_TEMP = (
    "INSERT INTO temperatures(room_id, temperature,date)VALUES(%s,%s,%s);"
)

GLOBAL_NUMBER_OF_DAYS = (
    """"SELECT COUNT(DISTINCT DATE(date)) AS days FROM temperatures;"""
)
GLOBAL_AVG = """SELECT AVG(temperature) as average FROM temperatures;"""


load_dotenv()
app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.route('/api/room',methods=['POST'])
def create_room():
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOMS_TABLE)
            cursor.execute(INSERT_ROOM_RETURN_ID,(name,))
            room_id = cursor.fetchone()
        return {"id":room_id,"message": f"Room {name} created."}, 201