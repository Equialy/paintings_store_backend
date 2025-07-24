from src.settings import settings
import urllib.parse
import secrets


async def generated_oauth_uri():
    query_params = {
        "client_id": settings.google_oauth.client_id,
        "redirect_uri": "http://localhost:3000/auth/google",
        "response_type": "code",
        "scope": " ".join(
            [
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/calendar",
                "openid",
                "profile",
                "email",
            ]
        ),
        "access_type": "offline",
    }
    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    return f"{base_url}?{query_string}"
