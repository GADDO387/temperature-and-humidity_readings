import serial
import MySQLdb
import time

# Configure the serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()

# Database connection
db = MySQLdb.connect(host="127.0.0.1", user="Gaddo", passwd="12345", db="sensor_data")
cur = db.cursor()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        if line:
            try:
                humidity, temp_c, temp_f = map(float, line.split(','))
                query = "INSERT INTO DHT11 (temperature, humidity, datetime) VALUES (%s, %s, NOW())"
                cur.execute(query, (temp_c, humidity))
                db.commit()
                print(f"Inserted: Humidity={humidity}, Temp_C={temp_c}")
            except ValueError:
                print("Invalid data received")
    time.sleep(1)

