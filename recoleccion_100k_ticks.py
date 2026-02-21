import requests
import time
import json
import os

API_URL = "https://api.deriv.com/ticks"  # Example API endpoint
FILE_PATH = "ticks_data.json"
CHECKPOINT_FILE = "checkpoint.txt"
TIMEOUT = 43200  # 12 hours in seconds

def collect_ticks():
    start_time = time.time()
    collected_ticks = []

    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            last_tick_id = int(f.read())
    else:
        last_tick_id = 0

    while len(collected_ticks) < 100000:
        if time.time() - start_time > TIMEOUT:
            print("12-hour timeout reached.")
            break
        
        try:
            response = requests.get(f"{API_URL}?start_id={last_tick_id}")
            response.raise_for_status()
            data = response.json()
            
            ticks = data.get("ticks", [])
            if ticks:
                collected_ticks.extend(ticks)
                last_tick_id = ticks[-1]['id']  # Update last tick id for checkpoint

                with open(CHECKPOINT_FILE, 'w') as f:
                    f.write(str(last_tick_id))

                print(f"Collected {len(collected_ticks)} ticks...")

            time.sleep(1)  # Respect API rate limits, adjust as necessary
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            time.sleep(5)  # Wait before retrying on error

    with open(FILE_PATH, 'w') as f:
        json.dump(collected_ticks, f)

    print("Collection complete. Total ticks collected:", len(collected_ticks))

if __name__ == "__main__":
    collect_ticks()