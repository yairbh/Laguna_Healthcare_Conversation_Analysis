
"""
This script contains constants that are needed throughout the project.
"""

import os

import pandas as pd

# Determine the project's root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create raw_data_df DataFarme
raw_data_file = os.path.join(project_root, 'data', 'processed', 'all_raw_utterances_df.csv')

if os.path.exists(raw_data_file):
    raw_data_df = pd.read_csv(raw_data_file)
else:
    raise FileNotFoundError(f"File not found: {raw_data_file}")


# Dictionary mapping numbers to topic names
TOPIC_MAP = {
    1: 'Member Identification',
    2: 'Call Recording Disclosure',
    3: 'Participant Verification',
    4: 'CM Introduction',
    5: 'Handling PHI',
    6: 'TCPA Compliance',
    7: 'Sensitive Information Protocol',
    8: 'Medical Consultation/Advice',
    9: 'Care Coordination',
    10: 'Log Protocol',
    11: 'Treatment Compliance/Medical State'
}

# List of special stop words
MY_STOPS = ['um', 'uh', 'affirmative', 'laugh', 'mmhmm', 'oh', 'hello', 'hi', 'okay', 'ok']

# File with USA cities names
cities_file = os.path.join(project_root, 'src', 'data', 'us_cities.csv')
