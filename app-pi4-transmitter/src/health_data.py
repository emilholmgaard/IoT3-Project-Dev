import re

PATTERNS = {
    "vgt": r"Personen vejer (\d+)\s?kg\.",
    "bt": r"Blodtrykket er (\d+)\s?over\s?(\d+)\.",
    "tmp": r"Kropstemperaturen er ([\d\.]+)\s?grader\.",
    "hf": r"Hjertefrekvensen er (\d+)\s?slag per minut\.",
    "rf": r"Respirationsfrekvensen er (\d+)\s?åndedrag per minut\.",
    "bs": r"Blodsukkeret er ([\d\.]+)\s?(mmol/L|millimol per liter|mmol pr\. liter)\."
}


def extract_health_data(text):
    extracted_data = {}
    for param, pattern in PATTERNS.items():
        match = re.search(pattern, text)
        if match:
            extracted_data[param] = (
                match.groups() if len(match.groups()) > 1 else match.group(1)
            )
    return extracted_data
