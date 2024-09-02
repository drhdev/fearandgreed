#!/usr/bin/env python3
# fearandgreed.py
# Version: 0.1
# Author: drhdev
# License: GPL v3
#
# Description:
# This script fetches the latest value and indications of the CNN Fear and Greed Index
# and stores the data in a JSON file.

import os
import requests
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import sys

# Configuration and Settings
base_dir = os.getcwd()  # Dynamically set to the current working directory
data_dir = os.path.join(base_dir, 'feargreed_data')  # Directory to store JSON files
log_filename = os.path.join(base_dir, 'feargreed.log')
url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Set up logging
logger = logging.getLogger('fearandgreed.py')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(log_filename, maxBytes=5 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Check for verbose flag
verbose = '-v' in sys.argv

if verbose:
    # Add console handler if verbose mode is enabled
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def setup_directories():
    """
    Ensures that the necessary directories are set up.
    """
    try:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logger.info(f"Directory {data_dir} created successfully.")
    except Exception as e:
        logger.error(f"Error setting up directory {data_dir}: {e}")
        sys.exit(1)

def error_exit(message):
    """
    Logs the error message and exits the script.
    """
    logger.error(message)
    sys.exit(1)

def fetch_fear_and_greed_data():
    """
    Fetches the latest Fear and Greed index data from CNN.
    """
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        logger.info("Successfully fetched data from the URL")

        if 'fear_and_greed' not in data or 'score' not in data['fear_and_greed']:
            error_exit("Unexpected JSON structure")

        current_data = {
            "score": data['fear_and_greed']['score'],
            "rating": data['fear_and_greed']['rating'],
            "timestamp": data['fear_and_greed']['timestamp']
        }
        return current_data
    except requests.exceptions.RequestException as e:
        error_exit(f"Request error: {e}")
    except ValueError as ve:
        error_exit(f"Data error: {ve}")
    except Exception as e:
        error_exit(f"An unexpected error occurred: {e}")

def save_data_to_json(data):
    """
    Saves the fetched Fear and Greed index data to a JSON file.
    """
    if data:
        filename = os.path.join(data_dir, datetime.now().strftime("fear_and_greed_%Y%m%d_%H%M%S.json"))
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save data to {filename}: {e}")
    else:
        logger.warning("No data to save.")

def main():
    """
    Main function that fetches and saves the Fear and Greed index data.
    """
    logger.info("Script started")

    # Set up necessary directories
    setup_directories()

    # Fetch data
    data = fetch_fear_and_greed_data()

    # Save data to JSON
    save_data_to_json(data)

    logger.info("Script finished")

if __name__ == "__main__":
    main()
