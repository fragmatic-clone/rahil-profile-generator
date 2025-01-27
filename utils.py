import json, uuid, os, random
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f"{current_dir}/data")
print("Data Directory created successfully.")

# SET THE SCOPE AND SOURCE SITE DOMAIN
scope = os.getenv("SCOPE", "systemscope")
domain = os.getenv("DOMAIN", "http://localhost:8085")
exist_segments = os.getenv("EXIST_SEGMENTS", "").split(",")
is_integration = os.getenv("INTEGRATION", "False")

# GENERATOR TRACK COUNTERS
profile_count = 0
session_count = 0
event_count = 0

data_dir = [
    "profileProperties",
    "sessionProperties"
]
profile_properties = {}
session_properties = {}

# ======= LOAD DATA ======
for folderName in data_dir:
    folder_path = os.path.join(current_dir, folderName)
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

    for file_name in all_files:
        file_path = os.path.join(current_dir, folderName, file_name)

        with open (file_path,'r') as profile_data:
            property_name = file_name.split('.')[0]
            if folderName == 'profileProperties':
                profile_properties[property_name] = json.load(profile_data)
            else:
                session_properties[property_name] = json.load(profile_data)

def generate_profile(is_known,current_date):
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
                "_countryCode": 'US' if is_integration == "True" else random.choice(profile_properties['countries-code'])
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
            },
            "segments": exist_segments,  
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
                    "status": 'GRANTED' if is_integration == "True" else random.choice(profile_properties['others']['consent_status']),
                    "statusDate": "2027-03-04T04:16:37Z",
                    "revokeDate": "2028-03-04T04:16:37Z"
                },
                f"{scope}/GDPR:Strictly Necessary Cookies": {
                    "scope":  scope,
                    "typeIdentifier": "GDPR:Strictly Necessary Cookies",
                    "status": 'GRANTED' if is_integration == "True" else random.choice(profile_properties['others']['consent_status']),
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

def generate_event(session_id, profile_id, consents, current_date):
    event_id = str(uuid.uuid4())

    old_event = {
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
                "mappingId": str(uuid.uuid4()),
                "consents": [{
                    "scope": value["scope"],
                    "status": value["status"],
                    "revokeDate": value["revokeDate"],
                    "statusDate": value["statusDate"],
                    "typeIdentifier": value["typeIdentifier"]
                }
                for value in consents.values()]
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
    event = {
        "_index": f"context-event-date-{current_date[:10].replace('-', '')}",
        "_type": "_doc",
        "_id": event_id,
        "_score": 1.0,
        "_source": {
            "scope": scope,
            "itemId": event_id,
            "itemType": "event",
            "eventType": "modifyConsent",
            "profileId": profile_id,
            "sessionId": session_id,
            "timeStamp": current_date,
            "properties": {
                "type": "modifyConsent",
                "origin": "http://127.0.0.1:8888",
                "consents": [{
                        "scope": value["scope"],
                        "status": value["status"],
                        "revokeDate": value["revokeDate"],
                        "statusDate": value["statusDate"],
                        "typeIdentifier": value["typeIdentifier"]
                    }
                    for value in consents.values()],
                "mappingId": str(uuid.uuid4()),
                "displayName": "Consent"
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
    session_id = str(uuid.uuid4())

    # Generate events for the session
    generate_event(
        session_id, 
        profile['_id'], 
        profile['_source']['consents'], 
        current_date
    )
    country = profile['_source']["properties"].get('_countryCode','')
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
