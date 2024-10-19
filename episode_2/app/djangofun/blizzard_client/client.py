import requests
from django.conf import settings


class BlizzardClient:
    def __init__(self):
        self.client_id = settings.BLIZZARD_CLIENT_ID
        self.client_secret = settings.BLIZZARD_CLIENT_SECRET

    def get(self, *args, **kwargs):
        # Get access token
        access_token = (
            requests.post(
                "https://oauth.battle.net/token",
                params={"grant_type": "client_credentials"},
                auth=(self.client_id, self.client_secret),
            )
            .json()
            .get("access_token")
        )

        return requests.get(
            *args, **kwargs, headers={"Authorization": f"Bearer {access_token}"}
        )
