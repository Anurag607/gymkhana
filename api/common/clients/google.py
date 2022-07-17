from typing import Any, Mapping

from google_auth_oauthlib.flow import Flow
from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token


class GoogleClient:
    """Client to connect to google APIs."""

    def __init__(self, id, secret):
        self.id = id
        self.secret = secret

    def verify_id_token(self, google_id_token: str) -> Mapping[str, Any]:
        """Returns verified data in `google_id_token` JWT.
        Throws:
            `ValueError` if `google_id_token` verification fails.
            `GoogleAuthError` if issuer is invalid.
        """

        return id_token.verify_oauth2_token(google_id_token, requests.Request(), clock_skew_in_seconds=5)

    def exchange_auth_code_for_token(self, code: str):
        client_config = {
            'installed':
                {'client_id': self.id, 'client_secret': self.secret,
                 'redirect_uris': ['http://localhost'],
                 'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                 'token_uri': 'https://accounts.google.com/o/oauth2/token', }}
        flow = Flow.from_client_config(
            client_config,
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.profile',
                    'https://www.googleapis.com/auth/userinfo.email'],
            redirect_uri='http://localhost:3000/login/redirect')

        return flow.fetch_token(code=code)


google_client = GoogleClient(settings.GOOGLE_OAUTH2_CLIENT_ID, settings.GOOGLE_OAUTH2_CLIENT_SECRET)

__all__ = ['google_client']
