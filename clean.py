import sys
from firebase_admin import auth, initialize_app
from firebase_admin.exceptions import FirebaseError

def main(project_id):
    """
    Delete all users from one Firebase project.
    """
    app = initialize_app(options={
        'projectId': project_id,
    }, name='app')

    # Start listing users from the beginning, 1000 at a time.
    print(f"Listing users from {project_id} Firebase project...")
    page = auth.list_users(app=app)
    users_to_delete = []
    while page:
        for user in page.users:
            if user.email:
                users_to_delete.append(user.uid)

        # Get next batch of users.
        page = page.get_next_page()
    
    print(f"Found {len(users_to_delete)} users to delete.")
    try:
        result = auth.delete_users(users_to_delete, app=app)
        for err in result.errors:
            print('Failed to delete user:', err.reason)
    except FirebaseError as error:
        print('Error importing users:', error)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise "Usage: python clean.py <project_id>"
    main(sys.argv[1])