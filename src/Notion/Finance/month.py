from src.Notion.Base import Finance


class Month(Finance):

    def __init__(self, bearer_token):
        super().__init__(bearer_token)
        self.database_id = self.env[f"FINANCE_DB_{__class__.__name__}"]

    def __str__(self):
        return f"Database id [{__class__.__name__}]: {self.database_id}"

    def get_by_date(self, find_date, display=True):

        find_date_split = find_date.split("-")
        y = str(find_date_split[0])
        m = int(find_date_split[1])

        if not self.database_id:
            raise Exception("No database ID could be found.")

        response = self.fetch_database(
            database_id=self.database_id,
            json_filter={
                "filter": {
                    "and": [
                        {"property": "Month", "formula": {"number": {"equals": m}}},
                        {"property": "Year", "formula": {"string": {"equals": y}}},
                    ]
                }
            },
        )

        datas = response.json()

        if display:
            print("---")
            for data in datas["results"]:
                print(f"ID: {data['id']}")
                print(f"Month: {data['properties']['Month']['formula']['number']}")
                print(f"Year: {data['properties']['Year']['formula']['string']}")
                print(f"Name: {data['properties']['Name']['title'][0]['plain_text']}")
                print("---")

        return datas["results"]
