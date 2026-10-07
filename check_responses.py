import requests
import re
import csv
import os
from datetime import datetime, timezone

URL = "https://brasilparticipativo.presidencia.gov.br/processes/consultas-publicas-conitec/f/5686/"

# Download the page
response = requests.get(
    URL,
    timeout=30,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)
response.raise_for_status()

# Look for "Respostas" and the number associated with it
text = response.text

match = re.search(r'(\d[\d.]*)\s*Respostas', text, re.IGNORECASE)

if not match:
    raise Exception("Could not find the response count on the page.")

# Convert Brazilian-style number like 3.204 into 3204
responses = int(match.group(1).replace(".", "").replace(",", ""))

# Current UTC time
timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

# Create CSV if it doesn't exist
file_exists = os.path.exists("responses.csv")

with open("responses.csv", "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow(["timestamp", "responses"])

    writer.writerow([timestamp, responses])

print(f"{timestamp} → {responses} respostas")
