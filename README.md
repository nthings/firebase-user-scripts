# Firebase User Migration and Deletion Scripts

This README.md provides an overview and usage instructions for two Python scripts that facilitate user management in Firebase projects. The first script is for migrating users from one Firebase project to another, while the second script is for deleting all users from a Firebase project.

## Prerequisites

Before using the scripts, make sure you have the following:

- Python installed on your system.
- Dependencies. You can install them using pip:
    ```
    pip install -r requirements.txt
    ```

## Script 1: User Migration

### Usage

To use the user migration script, follow the steps below:

1. Replace `<source_project_id>` and `<destination_project_id>` in the script with your actual Firebase project IDs. These IDs correspond to the source and destination Firebase projects, respectively.

2. Run the script using the following command:

   ```
   python migration.py <source_project_id> <destination_project_id>
   ```

### How It Works

1. The script initializes connections to both the source and destination Firebase projects.

2. It lists users from the source Firebase project and retrieves them in batches of 1000.

3. For each user, it checks if the user's email exists in the destination Firebase project.

4. If the user's email does not exist in the destination project, it adds the user to the migration list.

5. Basic user information and provider data are extracted from the source user and used to create an `ImportUserRecord` object.

6. The script then imports the list of users to the destination Firebase project using a hashing algorithm (standard scrypt) to securely handle password hashes.

7. If there are any errors during the user import process, they will be printed to the console.

Please use this script responsibly and ensure that you have the necessary permissions and access rights to both Firebase projects before running the migration.

**Note:** The script requires proper configuration of Firebase Admin SDK with the necessary credentials for both projects.

**Disclaimer:** This script is provided as-is and is not officially supported by Firebase or its affiliates. Use it at your own risk.

## Script 2: User Deletion

### Usage

To use the user deletion script, follow the steps below:

1. Replace `<project_id>` in the script with your actual Firebase project ID.

2. Run the script using the following command:

   ```
   python clean.py <project_id>
   ```

### How It Works

1. The script initializes a connection to the Firebase project specified by `<project_id>`.

2. It lists all the users from the Firebase project and retrieves them in batches of 1000.

3. For each user, it checks if the user has an email associated with their account and adds their UID to the list of users to be deleted.

4. After compiling the list of users to delete, the script proceeds with the deletion process.

5. The script attempts to delete the users in batches and handles any errors that occur during the deletion process.

Please use this script with caution as it will permanently delete all users from the specified Firebase project. Ensure that you have the necessary permissions and access rights to perform this action.

**Note:** The script requires proper configuration of Firebase Admin SDK with the necessary credentials for the specified project.

**Disclaimer:** This script is provided as-is and is not officially supported by Firebase or its affiliates. Use it at your own risk.
