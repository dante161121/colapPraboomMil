import time
import json
import requests
from google.colab import drive
from datetime import datetime, timedelta

# Mount Google Drive
drive.mount('/content/drive')

class SessionManager:
    def __init__(self, duration_hours=3):
        self.duration = timedelta(hours=duration_hours)
        self.start_time = datetime.utcnow()
    
    def is_time_over(self):
        return datetime.utcnow() - self.start_time > self.duration

# Function to handle API calls with retries
def resilient_api_call(url, params=None, retries=5):
    for i in range(retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            if i < retries - 1:
                time.sleep(2 ** i)  # Exponential backoff
            else:
                raise  # Move on if all retries fail

# Function to validate ticks data
def validate_tick(tick):
    return isinstance(tick, dict) and 'value' in tick and isinstance(tick['value'], (int, float))

# Main data collection function
def collect_ticks(target_count=100000):
    ticks_collected = []
    session_manager = SessionManager()

    while len(ticks_collected) < target_count:
        if session_manager.is_time_over():
            # Save progress
            with open('/content/drive/My Drive/ticks_checkpoint.json', 'w') as f:
                json.dump(ticks_collected, f)
            print("Session expired, progress saved.")
            break
        
        # Simulate API call to collect a tick
        tick = resilient_api_call('https://api.example.com/get_tick')

        if validate_tick(tick):
            ticks_collected.append(tick)
        else:
            print("Invalid tick received, skipping.")

    # Final save if completed
    if len(ticks_collected) == target_count:
        with open('/content/drive/My Drive/ticks_data.json', 'w') as f:
            json.dump(ticks_collected, f)
        print("Data collection completed successfully.")
    else:
        print("Data collection incomplete. Data saved:", len(ticks_collected))

if __name__ == "__main__":
    collect_ticks()