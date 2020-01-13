from typing import List
import secrets
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""


TOKEN = None


def check_TokenAuth(token):
    global TOKEN
    if not TOKEN:
        try:
            with open('api-token', 'r') as f:
                TOKEN = f.readline().strip()
        except:
            TOKEN = secrets.token_hex(32)
            with open('api-token', 'w') as f:
                f.write(f'{TOKEN}\n')
    # Constant-time token comparison
    if secrets.compare_digest(token, TOKEN):
        # Not using auth scopes in this project, so empty dict
        return {}
    # None = auth failed
    return None


