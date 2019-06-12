import csv
import re
from typing import Dict, List, Optional

import requests

from . import exceptions
from .models import TimeBooking


class Papierkram:
    subdomain: str = None
    session: requests.Session = None

    def __init__(self, subdomain: str, email: str, password: str):
        self.subdomain = subdomain
        self.session = requests.Session()
        self.login(email, password)

    def get_url(self, path: str):
        return f"https://{self.subdomain}.papierkram.de/{path}"

    def login(self, email: str, password: str) -> bool:
        auth_token_response = self.request("login")
        auth_token = re.findall(
            r'<meta content="([^"]+)" name="csrf-token" />',
            auth_token_response.content.decode("utf-8"),
        )
        if not auth_token:
            raise exceptions.PapierkramAuthException("No csrf-token found")

        login_response = self.request(
            "login",
            data=dict(
                [
                    ("authenticity_token", auth_token[0]),
                    ("user[subdomain]", self.subdomain),
                    ("user[email]", email),
                    ("user[password]", password),
                ]
            ),
        )

        if login_response.status_code != 302:
            raise exceptions.PapierkramAuthException("Invalid credentials")

        return True

    def request(
        self, path: str, query: Optional[Dict] = None, data: Optional[Dict] = None
    ) -> requests.Response:
        method = self.session.post if data else self.session.get
        return method(self.get_url(path), data=data or query, allow_redirects=False)

    def request_csv(self, path: str, query: Optional[Dict] = None) -> csv.DictReader:
        response = self.request(path, query=query)
        return csv.DictReader(response.content.decode("utf-8").splitlines(), delimiter=";")

    def timebookings(
        self, billed: bool = False, project_id: Optional[int] = None
    ) -> List[TimeBooking]:
        query = {
            "b": "billed" if billed else "unbilled",
            "project_id": str(project_id) if project_id else "",
        }
        return [
            TimeBooking.from_csv(record)
            for record in self.request_csv("zeiterfassung/buchungen.csv", query)
        ]
