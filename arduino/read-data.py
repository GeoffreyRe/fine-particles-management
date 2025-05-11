import serial
import requests
import time
from datetime import datetime

SERIAL_PORT = 'COM3'
BAUD_RATE = 9600
POST_URL = 'http://localhost:8000/api/measurements'
INTERVAL = 1

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    print(f"Connecté à {SERIAL_PORT}")
except serial.SerialException as e:
    print(f"Erreur de connexion série : {e}")
    exit(1)

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print("Donnée brute :", line)

            if "PM2.5" in line and "PM10" in line:
                try:
                    parts = line.split("|")
                    pm25 = float(parts[0].split(":")[1].replace("µg/m³", "").strip())
                    pm10 = float(parts[1].split(":")[1].replace("µg/m³", "").strip())

                    data = {"pm25": pm25, "pm10": pm10}
                    for fp_type in ["PM2.5", "PM10"]:
                        data = {
                            "unit": "µg/m³",
                            "type": fp_type,
                            "value": pm25 if fp_type == 'PM2.5' else pm10,
                            "time": datetime.now().isoformat(),

                        }
                        response = requests.post(POST_URL, json=data)
                        print(f"Envoyé à {POST_URL} : {data} → Réponse {response.status_code}")
                
                except Exception as e:
                    print("Erreur de parsing/envoi :", e)

        time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nArrêt manuel.")
        ser.close()
        break
