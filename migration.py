import sys
from firebase_admin import auth, initialize_app
from firebase_admin.exceptions import FirebaseError

def main(source_project_id, destination_project_id):
    """
    Migrate users from one Firebase project to another.
    """
    source_app = initialize_app(options={
        'projectId': source_project_id,
    }, name='source_app')

    destination_app = initialize_app(options={
        'projectId': destination_project_id,
    }, name='destination_app')

    # Start listing users from the beginning, 1000 at a time.
    print(f"Listing users from {source_project_id} Firebase project...")
    page = auth.list_users(app=source_app)
    users_to_migrate = []
    while page:
        for user in page.users:
            if user.email:
                try:
                    auth.get_user_by_email(user.email, app=destination_app)
                    print(f"User {user.email} already exists in {destination_project_id} Firebase project.")
                except auth.UserNotFoundError:
                    print(f"User {user.email} doesn't exists in {destination_project_id} Firebase project. Adding to migration list.")   
                    import_user_kwargs = {}
                    if user.uid: import_user_kwargs['uid'] = user.uid
                    if user.email: import_user_kwargs['email'] = user.email
                    if user.email_verified: import_user_kwargs['email_verified'] = user.email_verified
                    if user.display_name: import_user_kwargs['display_name'] = user.display_name
                    if user.phone_number: import_user_kwargs['phone_number'] = user.phone_number
                    if user.photo_url: import_user_kwargs['photo_url'] = user.photo_url
                    if user.disabled: import_user_kwargs['disabled'] = user.disabled
                    if user.user_metadata: import_user_kwargs['user_metadata'] = user.user_metadata
                    if user.provider_data:
                        provider_data = []
                        for p_data in user.provider_data:
                            provider_data_kwargs = {}
                            if p_data.uid: provider_data_kwargs['uid'] = p_data.uid
                            if p_data.display_name: provider_data_kwargs['display_name'] = p_data.display_name
                            if p_data.email: provider_data_kwargs['email'] = p_data.email
                            if p_data.photo_url: provider_data_kwargs['photo_url'] = p_data.photo_url
                            if p_data.provider_id: provider_data_kwargs['provider_id'] = p_data.provider_id
                            if p_data.phone_number: provider_data_kwargs['phone_number'] = p_data.phone_number
                            provider_data.append(auth.UserProvider(**provider_data_kwargs))
                        import_user_kwargs['provider_data'] = provider_data
                    if user.custom_claims: import_user_kwargs['custom_claims'] = user.custom_claims
                    if user.password_hash: import_user_kwargs['password_hash'] = user.password_hash.encode()
                    if user.password_salt: import_user_kwargs['password_salt'] = user.password_salt.encode()   
                    users_to_migrate.append(auth.ImportUserRecord(**import_user_kwargs))
        print("\n")
        # Get next batch of users.
        page = page.get_next_page()
    
    print(f"Found {len(users_to_migrate)} users to migrate.")
    print("\n")
    print(f"Starting migration from {source_project_id} to {destination_project_id} Firebase project...")
    hash_alg = auth.UserImportHash.standard_scrypt(
    memory_cost=1024, parallelization=16, block_size=8, derived_key_length=64)
    try:
        result = auth.import_users(users_to_migrate, hash_alg=hash_alg, app=destination_app)
        for err in result.errors:
            print('Failed to import user:', err.reason)
    except FirebaseError as error:
        print('Error importing users:', error)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise "Usage: python migration.py <source_project_id> <destination_project_id>"
    main(sys.argv[1], sys.argv[2])