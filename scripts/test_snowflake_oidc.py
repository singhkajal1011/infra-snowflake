import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import snowflake.connector


def required_environment_variable(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set.")
    return value


def get_github_oidc_token() -> str:
    request_url = required_environment_variable("ACTIONS_ID_TOKEN_REQUEST_URL")
    request_token = required_environment_variable("ACTIONS_ID_TOKEN_REQUEST_TOKEN")
    separator = "&" if "?" in request_url else "?"
    url = f"{request_url}{separator}{urlencode({'audience': 'snowflakecomputing.com'})}"
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {request_token}",
            "Accept": "application/json",
        },
    )

    with urlopen(request, timeout=30) as response:
        token = json.load(response).get("value")
    if not isinstance(token, str) or not token:
        raise RuntimeError("GitHub did not return an OIDC token.")
    return token


def main() -> None:
    connection_options = {
        "account": required_environment_variable("SNOWFLAKE_ACCOUNT"),
        "user": required_environment_variable("SNOWFLAKE_USER"),
        "authenticator": "WORKLOAD_IDENTITY",
        "workload_identity_provider": "OIDC",
        "token": get_github_oidc_token(),
    }
    role = os.getenv("SNOWFLAKE_ROLE")
    if role:
        connection_options["role"] = role

    connection = snowflake.connector.connect(**connection_options)
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT()")
            current_user, current_account = cursor.fetchone()
            print(
                "Snowflake OIDC authentication succeeded "
                f"(user={current_user}, account={current_account})."
            )
        finally:
            cursor.close()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
