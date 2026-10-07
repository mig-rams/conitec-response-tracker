import requests
import re
import csv
import os
import time
from datetime import datetime, timezone

URL = "https://brasilparticipativo.presidencia.gov.br/processes/consultas-publicas-conitec/f/5686/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}

# Try several times in case the government server temporarily
# closes the connection.
for attempt in range(5):
    try:
        response = requests.get(
            URL,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()
        break

    except requests.exceptions.SSLError as e:
        print(f"SSL error, attempt {attempt + 1}/5")

        if attempt == 4:
            raise

        time.sleep(5)

# Search the downloaded page for the response count
text = response.text

match = re.search(
    r'(\d[\d.]*)\s*Respostas',
    text,
    re.IGNORECASE
)

if not match:
    raise Exception("Could not find 'Respostas' on the page.")

responses = int(
    match.group(1)
    .replace(".", "")
    .replace(",", "")
)

timestamp = datetime.now(timezone.utc).strftime(
    "%Y-%m-%d %H:%M:%S UTC"
)

file_exists = os.path.exists("responses.csv")

with open(
    "responses.csv",
    "a",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    if not file_exists:
        writer.writerow(["timestamp", "responses"])

    writer.writerow([timestamp, responses])

print(f"{timestamp} → {responses} respostas")
