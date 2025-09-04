from dotenv import dotenv_values
import requests
from typing import Dict


class Notion:

    def __init__(self, bearer_token):
        self._notion_version: str = "2022-06-28"
        self._bearer_token: str = bearer_token
        self.env: Dict[str, str | None] = dotenv_values(".env.shared")

    def __str__(self):
        db_id = "".join([f"\n\t- {k}: {v}" for k, v in self.env.items()])
        return f"Database id [{__class__.__name__}]: {db_id}"

    def fetch_database(self, database_id: str, json_filter=None):
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        headers = {
            "Authorization": f"Bearer {self._bearer_token}",
            "Content-Type": "application/json",
            "Notion-Version": self._notion_version,
        }

        if json_filter is not None:
            response = requests.post(url=url, headers=headers, json=json_filter)
        else:
            response = requests.post(url=url, headers=headers)

        return response

    def fetch_page(self, page_id: str):
        url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {self._bearer_token}",
            "Content-Type": "application/json",
            "Notion-Version": self._notion_version,
        }

        response = requests.get(url=url, headers=headers)

        return response
