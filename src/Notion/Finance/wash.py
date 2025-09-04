from src.Notion.Base import Finance
from src.Notion.Finance.month import Month

import requests

from datetime import date, datetime
import pandas

from pprint import pprint


class Wash(Finance):

    def __init__(self, bearer_token):
        super().__init__(bearer_token)
        self.database_id = self.env[f"FINANCE_DB_{__class__.__name__}"]
        self.month = Month(bearer_token)

    def __str__(self):
        return f"Database id [{__class__.__name__}]: {self.database_id}"

    def get_by_date(self, start_date, end_date, display=True):

        if not self.database_id:
            raise Exception("No database ID could be found.")

        response = self.fetch_database(
            database_id=self.database_id,
            json_filter={
                "filter": {
                    "and": [
                        {
                            "property": "Date",
                            "type": "date",
                            "date": {"on_or_after": start_date},
                        },
                        {
                            "property": "Date",
                            "type": "date",
                            "date": {"on_or_before": end_date},
                        },
                        {
                            "property": "Item",
                            "type": "select",
                            "select": {"equals": "🧺 ค่าซักผ้า"},
                        },
                    ]
                }
            },
        )

        datas = response.json()

        if display:
            print("---")
            for data in datas["results"]:
                pprint(data)
                print("---")

        return datas["results"]

    def create_by_date(self, start_date, end_date):
        print(f"Create {__class__.__name__} from {start_date} to {end_date}")

        sdate = date(*list(map(int, start_date.split("-"))))
        edate = date(*list(map(int, end_date.split("-"))))
        date_ranges = pandas.date_range(sdate, edate, freq="d").to_list()
        date_ranges = list(map(lambda x: x.strftime("%Y-%m-%d"), date_ranges))

        for date_day in date_ranges:

            # Verify if date not in Wed and Sat.
            #
            # 0 = Sat
            # 3 = Wed
            #
            verify_date = int(datetime.strptime(date_day, "%Y-%m-%d").strftime("%w"))
            if verify_date not in [0, 3]:
                continue

            print(f"Date: {date_day}")
            response = requests.post(
                url="https://api.notion.com/v1/pages/",
                headers={
                    "Authorization": f"Bearer {self._bearer_token}",
                    "Content-Type": "application/json",
                    "Notion-Version": self._notion_version,
                },
                json={
                    "parent": {"type": "database_id", "database_id": self.database_id},
                    "icon": {
                        "type": "external",
                        "external": {
                            "url": "https://www.notion.so/icons/arrow-up_red.svg"
                        },
                    },
                    "properties": {
                        "Budget Item": {
                            "type": "relation",
                            "relation": [
                                {"id": "b6d7ada1-6f97-4b77-9ee0-06242b6e2b8d"}
                            ],
                            "has_more": False,
                        },
                        "Item": {
                            "type": "select",
                            "select": {
                                "id": "IjRN",
                                "name": "🧺 ค่าซักผ้า",
                                "color": "blue",
                            },
                        },
                        "Tag": {
                            "type": "select",
                            "select": {
                                "id": "e4cc87de-a432-4758-9432-d120e1618c1c",
                                "name": "Small Bill",
                                "color": "yellow",
                            },
                        },
                        "I/O": {
                            "type": "select",
                            "select": {
                                "id": "7b9b12ad-a902-48bb-aed2-b029606f2089",
                                "name": "Out",
                                "color": "red",
                            },
                        },
                        "Date": {
                            "type": "date",
                            "date": {
                                "start": date_day,
                            },
                        },
                        "S. Month & Year": {
                            "type": "relation",
                            "relation": [
                                {
                                    "id": self.month.get_by_date(
                                        date_day, display=False
                                    )[0]["id"]
                                }
                            ],
                            "has_more": False,
                        },
                        "Name": {
                            "id": "title",
                            "type": "title",
                            "title": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": "SPEND",
                                    },
                                    "plain_text": "SPEND",
                                }
                            ],
                        },
                        "Amount": {
                            "type": "number",
                            "number": 30,
                        },
                    },
                },
            )

            result = response.json()
            print(f"ID: {result['id']}")
            print(f"Date: {result['properties']['Date']['date']['start']}")
            print("---")


if __name__ == "__main__":

    from dotenv import dotenv_values

    config = dotenv_values(".env.secret")
    wash = Wash(config["BEARER_TOKEN"])

    start_date = "2025-09-01"
    end_date = "2025-09-07"

    wash.create_by_date(start_date, end_date)
