from flask import Flask, jsonify
import sqlite3
import json
from threading import Thread
import digitalio
import board
import busio
import adafruit_rfm9x
import os
import time
from azure.storage.blob import BlobServiceClient
from threading import Timer

app = Flask(__name__)

RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.tx_power = 23

latest_message = None

BLOB_CONNECTION_STRING = "xxx"
BLOB_CONTAINER_NAME = "backup-container"
BLOB_FILE_NAME = "data.db"

def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device (
            id TEXT PRIMARY KEY,
            timestamp INTEGER,
            wifi_strength INTEGER,
            ip_address TEXT,
            temperature REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health (
            cpr TEXT PRIMARY KEY,
            device_id TEXT,
            weight INTEGER,
            systolic INTEGER,
            diastolic INTEGER,
            temperature REAL,
            heart_rate INTEGER,
            respiration_rate INTEGER,
            blood_sugar REAL,
            FOREIGN KEY (device_id) REFERENCES device (id)
        )
    """)
    conn.commit()
    conn.close()

init_db()

def insert_data(data):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    device_data = (
        data.get("id"),
        data.get("ts"),
        data.get("ws"),
        data.get("ip"),
        data.get("tmp")
    )
    cursor.execute("""
        INSERT OR REPLACE INTO device (id, timestamp, wifi_strength, ip_address, temperature)
        VALUES (?, ?, ?, ?, ?)
    """, device_data)

    cpr = data.get("qr")
    health_data = data.get("hd", {})
    health_record = (
        cpr,
        data.get("id"),
        health_data.get("vgt"),
        *health_data.get("bt", (None, None)),
        health_data.get("tmp"),
        health_data.get("hf"),
        health_data.get("rf"),
        health_data.get("bs")
    )
    cursor.execute("""
        INSERT OR REPLACE INTO health (cpr, device_id, weight, systolic, diastolic, temperature, heart_rate, respiration_rate, blood_sugar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, health_record)

    conn.commit()
    conn.close()

def lora_listener():
    global latest_message
    while True:
        packet = rfm9x.receive()
        if packet is not None:
            try:
                packet_text = str(packet, "ascii").strip()
                print(f"Modtaget (ASCII): {packet_text}")
                latest_message = packet_text
                message_data = json.loads(packet_text)
                insert_data(message_data)
            except json.JSONDecodeError:
                print("Ugyldig JSON.")
            except Exception as e:
                print(f"Fejl: {e}")

def backup_db_to_azure():
    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=BLOB_FILE_NAME)

    with open("/home/eeeg/Desktop/app-api-pi0-receiver/data.db", "rb") as data_file:
        blob_client.upload_blob(data_file, overwrite=True)

def schedule_backup():
    backup_db_to_azure()
    Timer(604800, schedule_backup).start()

@app.route("/")
def home():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, wifi_strength, ip_address, temperature
        FROM device
        ORDER BY timestamp DESC
        LIMIT 5
    """)
    recent_devices = [dict(row) for row in cursor.fetchall()]

    cursor.execute("""
        SELECT cpr, systolic, diastolic
        FROM health
        ORDER BY cpr DESC
        LIMIT 100
    """)
    health_data = [dict(row) for row in cursor.fetchall()]

    categories = {
        "Normal": 0,
        "Prehypertension": 0,
        "Hypertension Stage 1": 0,
        "Hypertension Stage 2": 0,
        "Hypertensive Crisis": 0
    }

    for row in health_data:
        systolic = row["systolic"]
        diastolic = row["diastolic"]
        if systolic is not None and diastolic is not None:
            if systolic < 120 and diastolic < 80:
                categories["Normal"] += 1
            elif 120 <= systolic < 130 and diastolic < 80:
                categories["Prehypertension"] += 1
            elif 130 <= systolic < 140 or 80 <= diastolic < 90:
                categories["Hypertension Stage 1"] += 1
            elif 140 <= systolic < 180 or 90 <= diastolic < 120:
                categories["Hypertension Stage 2"] += 1
            else:
                categories["Hypertensive Crisis"] += 1

    cursor.execute("SELECT COUNT(*) FROM device")
    total_devices = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT cpr) FROM health")
    total_cpr = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM health")
    total_health_data = cursor.fetchone()[0]

    cursor.execute("""
        SELECT timestamp, temperature
        FROM device
        ORDER BY timestamp ASC
    """)
    temperature_data = [{"timestamp": row["timestamp"], "temperature": row["temperature"]} for row in cursor.fetchall()]

    global latest_message
    total_lora_messages = 0
    if latest_message:
        total_lora_messages = 1

    conn.close()

    return jsonify({
        "devices": recent_devices,
        "health_data": health_data,
        "total_devices": total_devices,
        "total_cpr": total_cpr,
        "total_health_data": total_health_data,
        "total_lora_messages": total_lora_messages,
        "temperature_data": temperature_data,
        "categories": categories
    })

@app.route("/device/<id>")
def device_detail(id):
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM device WHERE id = ?", (id,))
    device = cursor.fetchone()
    cursor.execute("SELECT * FROM health WHERE device_id = ?", (id,))
    health_records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({
        "device": dict(device),
        "health_records": health_records
    })

@app.route("/person/<cpr>")
def person_detail(cpr):
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health WHERE cpr = ?", (cpr,))
    person_data = cursor.fetchone()
    conn.close()
    return jsonify({
        "person_data": dict(person_data)
    })

@app.route("/devices")
def all_devices():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM device")
    devices = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({"devices": devices})

@app.route("/health")
def all_health():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health")
    health_data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({"health_data": health_data})

@app.route("/latest_message")
def latest_message_route():
    return jsonify({"message": latest_message or "Venter på første besked..."})

if __name__ == "__main__":
    schedule_backup()
    lora_listener_thread = Thread(target=lora_listener, daemon=True)
    lora_listener_thread.start()
    app.run(host="0.0.0.0", port=5000)
