import adafruit_rfm9x
import digitalio
import board
import busio


RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.tx_power = 23


def send_lora_message(message):
    if len(message) <= 252:
        rfm9x.send(bytes(message + "\r\n", "utf-8"))
        print(f"{message}")
    else:
        print("Beskeden for stor.")
