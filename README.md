# Environment Variables Setup Guide

This guide provides instructions on setting up the necessary environment variables for the project. Follow these steps to configure your `.env` file:

## Instructions

1. **Create a `.env` file:**
   - In the root directory of the project, create a new file named `.env`.

2. **Add the following variables to your `.env` file:**

```bash
# Architecture Configuration
ARCHITECTURE=new # Set to 'new' for new architecture or 'old' for old architecture

# DynamoDB Configuration
DYNAMO_PROFILE_TABLE= # Set dynamodb profile table name

# AWS Configuration
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=

# PostgreSQL Configuration
PG_DB_NAME=
PG_DB_USER=
PG_DB_PASS=
PG_HOST=
PG_PORT=

# Elasticsearch Configuration # if using old arch
ES_BASE_URL=

# Fields Data
SCOPE= 
DOMAIN=
EXIST_SEGMENTS= # specify where you want to include generated profiles
INTEGRATION = False # Set "True" if need country=US and advertising_cookie=granted
```

3. **Replace placeholders with actual values:**
   - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: Provide your AWS credentials.
   - `PG_DB_NAME`, `PG_DB_USER`, `PG_DB_PASS`, `PG_HOST`: Fill in your PostgreSQL database details.

4. **Save the file:**
   - Ensure the `.env` file is saved and located in the root of your project.

5. **Verify Configuration:**
   - Run the application to confirm the environment variables are loaded correctly.

## Notes

- Do not share your `.env` file publicly as it contains sensitive information.
- Ensure `.env` is included in your `.gitignore` file to prevent it from being committed to the repository.

## Example `.gitignore` Entry

```
# Ignore .env file
.env
```