import re

import requests

from . import exceptions


class Papierkram:
    subdomain = None
    session = None

    def __init__(self, subdomain, email, password):
        self.subdomain = subdomain
        self.session = requests.Session()
        self.login(email, password)

    def get_url(self, path):
        return f'https://{self.subdomain}.papierkram.de/{path}'

    def login(self, email, password):
        auth_token_response = self.request('login')
        auth_token = re.findall(
            r'<meta content="([^"]+)" name="csrf-token" />',
            auth_token_response.content.decode('utf-8'),
        )
        if not auth_token:
            raise exceptions.PapierkramAuthException('No csrf-token found')

        login_response = self.request('login', data=dict([
            ('authenticity_token', auth_token[0]),
            ('user[subdomain]', self.subdomain),
            ('user[email]', email),
            ('user[password]', password)
        ]))

        if login_response.status_code != 302:
            raise exceptions.PapierkramAuthException('Invalid credentials')

        return True

    def request(self, path, query=None, data=None):
        method = self.session.post if data else self.session.get
        return method(self.get_url(path), data=data or query, allow_redirects=False)
