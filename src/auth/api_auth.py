def api_key_auth(api_key):
    # Verifica API key contro database
    user = database.get_user_by_api_key(api_key)
    return user if user else None