import random, os
from datetime import datetime, timedelta
from utils import generate_profile, generate_session
from old_arch import old_arch_runner
from new_arch import new_arch_runner
from dotenv import load_dotenv

load_dotenv()
# Generate profiles with both current and previous visit times ==================================
ARCHITECTURE = os.getenv("ARCHITECTURE", "new") 

current_dir = os.path.dirname(os.path.abspath(__file__))

total_profiles = 1 # TOTAL NUMBER OF PROFILES TO BE GENERATED
is_previous_date = True # BEFORE TODAY'S DATE
is_known = True # KNOWN PROFILE ( with all profile properties ) OR UNKNOWN PROFILE
month = 7 # PROFILE MONTH 
year = 2024 # PROFILE YEAR

for _ in range(total_profiles):
    if is_previous_date:
        # Define the start and end dates
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, 29)

        # Generate a random date
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

        # Generate random time components
        hours = random.randint(0, 23)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)
        microseconds = random.randint(0, 999999)

        # Combine date and time components
        current_date = random_date.replace(hour=hours, minute=minutes, second=seconds, microsecond=microseconds)
        current_date = current_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    else:
        current_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    profile = generate_profile(is_known,current_date)
    generate_session(profile,current_date)

print('==== DATA FOLDER LOADED SUCCESSFULLY! ====')

print(f"==== RUNNING <{ARCHITECTURE}> ARCHITECTURE ====")
new_arch_runner(current_dir) if ARCHITECTURE == 'new' else old_arch_runner(current_dir, is_previous_date, month, year)