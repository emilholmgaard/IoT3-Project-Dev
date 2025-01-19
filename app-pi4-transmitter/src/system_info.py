import subprocess
import socket
import re


def get_wifi_strength():
    try:
        result = subprocess.run(['iwconfig'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'Signal level' in line:
                signal_strength = re.search(r'Signal level=(-?\d+)', line)
                if signal_strength:
                    return signal_strength.group(1)
    except Exception:
        return None
    return None


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.254.254.254', 1))
        return s.getsockname()[0]
    except Exception:
        return None
    finally:
        s.close()


def get_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return round(float(f.read()) / 1000.0, 1)
    except Exception:
        return None
