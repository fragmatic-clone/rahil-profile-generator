import boto3
import lz4.frame
import json, os, shutil
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# AWS CREDENTIALS ====================
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
DYNAMO_PROFILE_TABLE = os.getenv("DYNAMO_PROFILE_TABLE")

# POSTGRES CREDENTIALS ================
PG_DB_NAME= os.getenv("PG_DB_NAME")
PG_DB_USER= os.getenv("PG_DB_USER")
PG_DB_PASS= os.getenv("PG_DB_PASS")
PG_HOST= os.getenv("PG_HOST")
PG_PORT= os.getenv("PG_PORT")

def batch_insert_into_postgres(profiles, key='profile'):
    """
    Insert multiple profiles into Postgres using a stored Procedure.
    """
    conn = None
    config = f"dbname='{PG_DB_NAME}' user='{PG_DB_USER}' password='{PG_DB_PASS}' host='{PG_HOST}' port='{PG_PORT}'"
    try:
        conn = psycopg2.connect(config)
        cur = conn.cursor()

        json_data = [json.dumps(item) for item in profiles]

        cur.execute(
            f"SELECT * from insert_{key}_data(%s::JSONB[])",
            [json_data]
        )
        conn.commit()

        result = cur.fetchall()
        print(f"Postgres Response: {result}")

    except (Exception, psycopg2.DatabaseError) as error:
      print("Error while connecting to PostgreSQL", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

def get_dynamodb_table(table_name):
    """
    Initialize a connection to DynamoDB and return the table resource.
    """
    try:
        # Initialize DynamoDB resource
        dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        # Get the table
        table = dynamodb.Table(table_name)
        print(f"Connected to DynamoDB table: {table_name}")
        return table
    except Exception as e:
        print("Error connecting to DynamoDB:", str(e))
        raise

def batch_insert_profiles_into_dynamo(table, profiles):
    """
    Insert multiple profiles into the DynamoDB table in a batch.
    """
    try:
        # Prepare batch write requests
        with table.batch_writer() as batch:
            for profile in profiles:
                # Convert Profile to JSON String
                json_data = json.dumps(profile)
                
                # Compress JSON Data using LZ4
                compressed_data = lz4.frame.compress(json_data.encode("utf-8"))
                
                # Prepare DynamoDB Record
                dynamo_record = {
                    "itemId": profile["itemId"],
                    "data": compressed_data,
                }
                
                # Add the record to the batch
                batch.put_item(Item=dynamo_record)

        print("Profiles inserted successfully into DynamoDB!")

    except Exception as e:
        print("Error inserting profiles into DynamoDB:", str(e))
        raise

def read_json_file(file_path):
    """Read a JSON file line by line and return a list of parsed objects."""
    try:
        data = []
        with open(file_path, "r") as file:
            for line in file:
                if line.strip():  # Ignore empty lines
                    _source = json.loads(line).get('_source')
                    if _source:
                        data.append(_source)
        return data
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return []

def new_arch_runner(current_dir):
    file_paths = {
        "profiles": os.path.join(current_dir, "data", "profileData.json"),
        "sessions": os.path.join(current_dir, "data", "sessionData.json"),
        "events": os.path.join(current_dir, "data", "eventData.json"),
    }
    # Read data from files
    profiles = read_json_file(file_paths["profiles"])
    sessions = read_json_file(file_paths["sessions"])
    events = read_json_file(file_paths["events"])

    
    # Connect to DynamoDB Table
    table = get_dynamodb_table(DYNAMO_PROFILE_TABLE)

    print('ADDING PROFILES TO DYNAMODB ....')
    batch_insert_profiles_into_dynamo(table, profiles)
    print('ADDED PROFILES TO DYNAMODB SUCCESSFULLY !')

    # Batch insert data into Postgres
    postgres_data = {
        "profile": profiles,
        "session": sessions,
        "event": events
    }

    for data_type, data in postgres_data.items():
        if data:
            print(f'ADDING {data_type.upper()}S TO POSTGRES ....')
            batch_insert_into_postgres(data, data_type)
            print(f'ADDED {data_type.upper()}S TO POSTGRES SUCCESSFULLY !')

    directory_path = f"{current_dir}/data"
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print('==== DATA FOLDER UNLOADED SUCCESSFULLY! ====')
    else:
        print("The Data directory does not exist.")
