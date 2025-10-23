"""Utility functions for the resolutions agent."""

import requests


def get_token(client_id, client_secret, scope):
    """Get an OAuth2 token using client credentials."""
    resp = requests.post(
        # TODO externalize this
        'https://identity.service.homedepot.dev/oauth2/v1/token',
        data={
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': scope,
        },
    )
    resp.raise_for_status()
    return resp.json()['access_token']


def read_instructions_from_file(filepath):
    """Read instructions from a file."""
    with open(filepath, encoding='utf-8') as file:
        return file.read()


def get_openapi_schema(url, client_id, client_secret, scope):
    """Get OpenAPI schema from a URL using OAuth2 client credentials."""
    token = get_token(client_id, client_secret, scope)
    return requests.get(
        url, headers={'Authorization': f'Bearer {token}'}
    ).json()
