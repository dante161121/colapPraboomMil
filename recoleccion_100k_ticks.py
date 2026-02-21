import time
import json
import requests

# Constants
API_URL = 'https://api.example.com/data'
DRIVE_STORAGE_PATH = '/content/drive/My Drive/Colab_Saves/'
COLLECTION_LIMIT = 100000
COLLECT_INTERVAL = 10  # seconds

# Function to collect data from API

def collect_data():
    collected_data = []
    for _ in range(COLLECTION_LIMIT):
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            data = response.json()
            collected_data.append(data)
            time.sleep(COLLECT_INTERVAL)  # Wait before next request
        except requests.exceptions.RequestException as e:
            print(f'Error collecting data: {e}')
            # Handle API connection error, e.g., exponential backoff, retries, etc.
            time.sleep(60)  # Wait 1 minute before retrying
    return collected_data

# Function to save data to Google Drive

def save_to_drive(data):
    filename = f'{DRIVE_STORAGE_PATH}collected_data_{int(time.time())}.json'
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f'Data saved to {filename}')

# Main execution flow

if __name__ == '__main__':
    collected_data = collect_data()
    save_to_drive(collected_data)