import json, uuid, random
from datetime import datetime, timedelta
import os, subprocess, shutil

# SET THE SCOPE AND SOURCE SITE DOMAIN
scope = "dgv"
domain = "https://dgv-frontend.ua.verbinteractive.com/"

profile_count = 0
session_count = 0
event_count = 0
current_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f"{current_dir}/data")
print("Data Directory created successfully.")

def generate_profile(is_known,current_date):

    all_files = [
        "fName.json",
        "lName.json",
        "countries.json",
        "nationality.json",
        "others.json"
    ]

    profile_properties = {}

    for file_name in all_files:

        file_path = os.path.join(current_dir, 'profileProperties', file_name)

        with open (file_path,'r') as profile_data:
            property_name = file_name.split('.')[0]
            profile_properties[property_name] = json.load(profile_data)

    # Define lists of possible values for certain properties
    profile_id = str(uuid.uuid4())

    profile = {
        "_index": "context-profile",
        "_type": "_doc",
        "_id": profile_id,
        "_score": 1.0,
        "_source": {
            "itemId": profile_id,
            "itemType": "profile",
            "properties": {
                "nbOfVisits": 1,
                "lastVisit": current_date,
                "firstVisit": current_date,
            },
            "systemProperties": {
                "lastUpdated": current_date,
                "firstSessionLat": 46.1884341,
                "scope":  scope,
                "domains": [domain],
                "type": random.choice(profile_properties['others']['type']),
                "eventTypes": ['sessionCreated", "view'],
                "visitedPages": ['/'],
                "firstDomain": domain,
                "firstSessionLon": 6.1282508,
                "latestCountry": random.choice(profile_properties['countries-code'])
            },
            "segments": [allProfile_segmentId],  
            "scores": {},
            "mergedWith": None,
            "consents": {
                f"{scope}/GDPR:Functional Cookies": {
                    "scope":  scope,
                    "typeIdentifier": "GDPR:Functional Cookies",
                    "status": random.choice(profile_properties['others']['consent_status']),
                    "statusDate": "2026-03-04T04:16:37Z",
                    "revokeDate": "2027-03-04T04:16:37Z"
                },
                f"{scope}/GDPR:Advertising Cookies": {
                    "scope":  scope,
                    "typeIdentifier": "GDPR:Advertising Cookies",
                    "status": random.choice(profile_properties['others']['consent_status']),
                    "statusDate": "2027-03-04T04:16:37Z",
                    "revokeDate": "2028-03-04T04:16:37Z"
                },
                f"{scope}/GDPR:Strictly Necessary Cookies": {
                    "scope":  scope,
                    "typeIdentifier": "GDPR:Strictly Necessary Cookies",
                    "status": random.choice(profile_properties['others']['consent_status']),
                    "statusDate": "2024-03-04T04:16:37Z",
                    "revokeDate": "2025-03-04T04:16:37Z"
                },
                f"{scope}/GDPR:Performance Cookies": {
                    "scope":  scope,
                    "typeIdentifier": "GDPR:Performance Cookies",
                    "status": random.choice(profile_properties['others']['consent_status']),
                    "statusDate": "2025-03-04T04:16:37Z",
                    "revokeDate": "2026-03-04T04:16:37Z"
                }
            }
        }
    }

    if is_known:

        fName = random.choice(profile_properties['fName'])
        lName = random.choice(profile_properties['lName'])

        properties = profile['_source']['properties']

        properties['zipCode'] = random.randint(100000, 999999)
        properties['address'] = f"H-no.{random.randint(1, 100)}, {fName} Street, {lName}"
        properties['phoneNumber'] = random.randint(1000000000, 9999999999)
        properties['firstName'] = fName
        properties['lastName'] = lName
        properties['email'] = f"{fName.lower()}{lName.lower()}{random.randint(100, 999)}@gmail.com"
        properties['gender'] = random.choice(profile_properties['others']['gender'])
        properties['dob'] = f"{random.randint(1980, 2000)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        properties['maritalStatus'] = random.choice(profile_properties['others']["marital_status"])
        properties['nationality'] = random.choice(profile_properties['nationality'])
        properties['age'] = random.randint(12, 110)


    file_path = os.path.join(current_dir, 'data', "profileData.json")

    with open(file_path, "a") as profile_file:
        profile_file.write(json.dumps(profile) + "\n")
    
    global profile_count
    profile_count += 1
    print(f"{profile_count} - Profile Generated")

    return profile

def generate_event(session_id, profile_id,current_date):
    event_id = str(uuid.uuid4())

    event = {
        "_index": f"context-event-date-{current_date[:10].replace('-', '')}",
        "_type": "_doc",
        "_id": event_id,
        "_score": 1.0,
        "_source": {
            "itemId": event_id,
            "itemType": "event",
            "scope":  scope,
            "eventType": "view",
            "sessionId": session_id,
            "profileId": profile_id,
            "timeStamp": current_date,
            "properties": {
                "origin": "http://localhost:8000",
                "mappingId": str(uuid.uuid4())
            },
            "source": {
                "itemId": "dgv",
                "itemType": "site",
                "scope":  scope,
                "properties": {}
            },
            "target": {
                "itemId": "/",
                "itemType": "page",
                "scope":  scope,
                "properties": {
                    "path": "/",
                    "pageInfo": {
                        "destinationURL": "http://localhost:8000/",
                        "categories": [],
                        "pageId": "/",
                        "pageName": "Review",
                        "referringURL": "",
                        "tags": []
                    },
                    "queryKeys": [],
                    "query": {}
                }
            }
        }
    }
    file_path = os.path.join(current_dir, 'data', "eventData.json")

    with open(file_path, "a") as event_file:
        event_file.write(json.dumps(event) + "\n")

    global event_count
    event_count += 1
    print(f"{event_count} - Event Generated")

    return event

def generate_session(profile,current_date):

    all_files = [
        "browserLanguage.json",
        "countryCode.json",
        "timezone.json",
        "others.json"
    ]

    session_properties = {}
    for file_name in all_files:

        file_path = os.path.join(current_dir, 'sessionProperties', file_name)

        with open (file_path,'r') as session_data:
            property_name = file_name.split('.')[0]
            session_properties[property_name] = json.load(session_data)

    session_id = str(uuid.uuid4())

    # Generate events for the session
    generate_event(session_id, profile['_id'],current_date)

    country = profile['_source']["systemProperties"].get('latestCountry','')
    city = session_properties['others']['cities']
    session = {
        "_index": f"context-session-date-{current_date[:10].replace('-', '')}",
        "_type": "_doc",
        "_id": session_id,
        "_score": 1.0,
        "_source": {
            "itemId": session_id,
            "itemType": "session",
            "scope":  scope,
            "profileId": profile['_id'],
            "profile": profile['_source'],
            "properties": {
                "sessionCity": city,
                "operatingSystemFamily": random.choice(session_properties['others']['os_families']),
                "userAgentNameAndVersion": f"{random.choice(session_properties['others']['browsers'])}@@{random.randint(1, 200)}.0.0.0",
                "source": "Direct",
                "userAgentName": random.choice(session_properties['others']['browsers']),
                "firstSource": random.choice(session_properties['others']['first_source']),
                "sessionCountryCode": random.choice(session_properties['countryCode']),
                "deviceName": f"{random.choice(session_properties['others']['os_families'])} {random.choice(session_properties['others']['browsers'])}",
                "referringURL": "",
                "sessionIsp": random.choice(session_properties['others']['session_isp']),
                "day": random.choice(session_properties['others']['days']),
                "browserLanguage": random.choice(session_properties['browserLanguage']),
                "ipAddress": "127.0.0.1",
                "countryAndCity": f"{country}@@{city}@@2660645@@6458783",
                "timeZone": random.choice(session_properties['timezone']),
                "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "sessionCountryName": country,
                "deviceCategory": "Desktop",
                "pageReferringURL": "",
                "userAgentVersion": f"{random.randint(1, 200)}.0.0.0",
                "sessionAdminSubDiv2": random.randint(1, 9999999),
                "sessionAdminSubDiv1": random.randint(1, 9999999),
                "location": {
                    "lon": 6.1282508,
                    "lat": 46.1884341
                },
                "operatingSystemName": random.choice(session_properties['others']['operating_systemName']),
                "deviceBrand": random.choice(session_properties['others']['device_brand'])
            },
            "systemProperties": {
                "eventTypes": ['sessionCreated", "view']
            },
            "timeStamp": current_date,
            "lastEventDate": current_date,
            "size": 2,
            "duration": 19620
        }
    }

    file_path = os.path.join(current_dir, 'data', "sessionData.json")

    with open(file_path, "a") as session_file:
        session_file.write(json.dumps(session) + "\n")

    global session_count
    session_count += 1
    print(f"{session_count} - Session Generated")

    return session

# Generate profiles with both current and previous visit times ==================================

is_previous_date = True # BEFORE TODAY'S DATE
is_known = True # KNOWN PROFILE ( with all profile properties ) OR UNKNOWN PROFILE
month = 7 # PROFILE MONTH 
year = 2024 # PROFILE YEAR
total_profiles = 2000 # TOTAL NUMBER OF PROFILES TO BE GENERATED
allProfile_segmentId = "3b79bef6" # All Profiles Segment Id

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

print('DATA FILESE GENERATED SUCCESSFULLY!')
esBaseUrl = 'http://localhost:9200'

if is_previous_date:
    if month < 10 :
        month = '0' + str(month)
    cxt_session = f'context-session-date-{year}-{month}'
    cxt_event = F'context-event-date-{year}-{month}'
else:
    cxt_session = f'context-session-date-2024-03'
    cxt_event = f'context-event-date-2024-03'

elasticdump_profile = ["elasticdump", f"--input={current_dir}/data/profileData.json", f"--output={esBaseUrl}/context-profile", "--type=data"]
elasticdump_session = ["elasticdump", f"--input={current_dir}/data/sessionData.json", f"--output={esBaseUrl}/{cxt_session}", "--type=data"]
elasticdump_event = ["elasticdump", f"--input={current_dir}/data/eventData.json", f"--output={esBaseUrl}/{cxt_event}", "--type=data"]

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
        print("Data Directory and its contents removed successfully.")
    else:
        print("The Data directory does not exist.")

except subprocess.CalledProcessError as e:
    print("Error executing elasticdump command:", e)