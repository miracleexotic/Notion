from src.Notion.Base import Finance
from src.Notion.Finance.month import Month
from src.Utils.pdf import extract_TTB_pdf, spend_traffic_data_format

import requests

from datetime import date
import pandas


class Transport(Finance):

    def __init__(self, bearer_token):
        super().__init__(bearer_token)
        self.database_id = self.env[f"FINANCE_DB_{__class__.__name__}"]
        self.month = Month(bearer_token)

    def __str__(self):
        return f"Database id [{__class__.__name__}]: {self.database_id}"

    def sum_price(self, data: str):
        note = data["properties"]["Note"]["rich_text"][0]["plain_text"]

        if not len(data["properties"]["Note"]["rich_text"]) or not note:
            return 0
        if note.startswith("#"):
            return data["properties"]["Amount"]["number"]

        amount = sum(list(map(lambda x: float(x.strip()), note.split(","))))
        print("total =", amount)

        return amount

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
                            "select": {"equals": "🚕 ค่าเดินทาง"},
                        },
                    ]
                }
            },
        )

        datas = response.json()

        if display:
            print("---")
            for data in datas["results"]:
                print(data["properties"]["Date"]["date"]["start"])
                print(data["properties"]["Note"]["rich_text"][0]["plain_text"])
                self.sum_price(data["properties"]["Note"]["rich_text"][0]["plain_text"])
                print(data["properties"]["Amount"]["number"])
                print("---")

        return datas["results"]

    def update_by_date(self, start_date, end_date):
        print(f"Update {__class__.__name__} from {start_date} to {end_date}")

        datas = self.get_by_date(start_date, end_date, display=False)

        for data in datas:

            print(data["properties"]["Date"]["date"]["start"])
            response = requests.patch(
                url=f"https://api.notion.com/v1/pages/{data['id']}",
                headers={
                    "Authorization": f"Bearer {self._bearer_token}",
                    "Content-Type": "application/json",
                    "Notion-Version": self._notion_version,
                },
                json={"properties": {"Amount": self.sum_price(data)}},
            )

            new_data = response.json()
            print(new_data["properties"]["Amount"]["number"])
            print("---")

    def create_by_date(self, start_date, end_date, file_ttb=None):
        print(f"Create {__class__.__name__} from {start_date} to {end_date}")

        sdate = date(*list(map(int, start_date.split("-"))))
        edate = date(*list(map(int, end_date.split("-"))))
        date_ranges = pandas.date_range(sdate, edate, freq="d").to_list()
        date_ranges = list(map(lambda x: x.strftime("%Y-%m-%d"), date_ranges))

        if file_ttb:
            items_by_date = extract_TTB_pdf(file_ttb)

        for date_day in date_ranges:

            print(f"Date: {date_day}")

            if file_ttb:
                try:
                    data = spend_traffic_data_format(items_by_date[date_day])
                except KeyError as e:
                    data = "0"
            else:
                data = "0"

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
                                {"id": "484298a2-a689-4cda-8ae3-69b4118911b3"}
                            ],
                            "has_more": False,
                        },
                        "Item": {
                            "type": "select",
                            "select": {
                                "id": "vUYj",
                                "name": "🚕 ค่าเดินทาง",
                                "color": "yellow",
                            },
                        },
                        "Tag": {
                            "type": "select",
                            "select": {
                                "id": "7a6a8346-32fc-443c-9148-8b2d3e91f287",
                                "name": "Daily Living",
                                "color": "green",
                            },
                        },
                        "Note": {
                            "type": "rich_text",
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": data,
                                    },
                                    "plain_text": data,
                                }
                            ],
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
                    },
                },
            )

            result = response.json()
            print(f"ID: {result['id']}")
            print(f"Date: {result['properties']['Date']['date']['start']}")
            print("---")
