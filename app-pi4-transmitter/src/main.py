import json
import time
from datetime import datetime
from lora import send_lora_message
from qr_code import scan_qr_code_live
from speech_recognition import recognize_from_microphone
from health_data import extract_health_data, PATTERNS
from system_info import get_wifi_strength, get_ip_address, get_temperature
import uuid
import RPi.GPIO as GPIO

BUTTON_PIN = 17

RASPBERRY_ID = str(uuid.uuid4())[:8]

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def wait_for_button_press():
    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        time.sleep(0.1)

def main():
    while True:
        wait_for_button_press()

        qr_code_data = scan_qr_code_live()
        if qr_code_data:
            recognized_speech = recognize_from_microphone()
            if recognized_speech:
                health_data = extract_health_data(recognized_speech)
                if health_data:
                    message_data = {
                        "id": RASPBERRY_ID,
                        "ts": int(time.time()),
                        "qr": qr_code_data,
                        "hd": health_data,
                        "ws": get_wifi_strength(),
                        "ip": get_ip_address(),
                        "tmp": get_temperature()
                    }
                    message_data = {k: v for k, v in message_data.items() if v is not None}
                    json_message = json.dumps(message_data, separators=(',', ':'))
                    send_lora_message(json_message)
        time.sleep(5)

if __name__ == "__main__":
    main()
    GPIO.cleanup()
