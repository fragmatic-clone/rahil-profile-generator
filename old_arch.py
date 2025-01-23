import os, subprocess, shutil
from dotenv import load_dotenv

load_dotenv()

ES_BASE_URL = os.getenv("ES_BASE_URL")

def old_arch_runner(current_dir, is_previous_date, month, year):
    if is_previous_date:
        if month < 10 :
            month = '0' + str(month)
        cxt_session = f'context-session-date-{year}-{month}'
        cxt_event = F'context-event-date-{year}-{month}'
    else:
        cxt_session = f'context-session-date-2024-03'
        cxt_event = f'context-event-date-2024-03'

    elasticdump_profile = ["elasticdump", f"--input={current_dir}/data/profileData.json", f"--output={ES_BASE_URL}/context-profile", "--type=data"]
    elasticdump_session = ["elasticdump", f"--input={current_dir}/data/sessionData.json", f"--output={ES_BASE_URL}/{cxt_session}", "--type=data"]
    elasticdump_event = ["elasticdump", f"--input={current_dir}/data/eventData.json", f"--output={ES_BASE_URL}/{cxt_event}", "--type=data"]

    try:
        print('ADDING PROFILES TO ELASTICSEARCH ....')
        result = subprocess.run(elasticdump_profile, capture_output=True, text=True, check=True)
        print("Elasticdump Profile Status:", result.stdout)

        print('ADDING SESSIONS TO ELASTICSEARCH ....')
        result = subprocess.run(elasticdump_session, capture_output=True, text=True, check=True)
        print("Elasticdump Session Status:", result.stdout)

        print('ADDING EVENTS TO ELASTICSEARCH ....')
        result = subprocess.run(elasticdump_event, capture_output=True, text=True, check=True)
        print("Elasticdump Event Status:", result.stdout)

        print('PROFILES & SESSIONs & EVENTS :: CREATED SUCCESSFULLY !')

        directory_path = f"{current_dir}/data"
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)
            print('==== DATA FOLDER UNLOADED SUCCESSFULLY! ====')
        else:
            print("The Data directory does not exist.")

    except subprocess.CalledProcessError as e:
        print("Error executing elasticdump command:", e)