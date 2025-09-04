from src.Notion.Base import Work
from pprint import pprint


class Todo(Work):

    def __init__(self, bearer_token):
        super().__init__(bearer_token)
        self.database_id = self.env[f"WORK_DB_{__class__.__name__}"]

    def __str__(self):
        return f"Database id [{__class__.__name__}]: {self.database_id}"

    def get_westcon(self):

        if not self.database_id:
            raise Exception("No database ID could be found.")

        response = self.fetch_database(
            database_id=self.database_id,
            json_filter={
                "filter": {
                    "and": [
                        {"property": "📚 Product", "relation": {"is_empty": True}},
                        {
                            "property": "🙋\u200d♂️ Customer",
                            "relation": {"is_empty": True},
                        },
                    ]
                }
            },
        )

        datas = response.json()

        results = {"Westcon": []}

        for i in datas["results"]:
            task = ""
            for j in i["properties"]["Name"]["title"]:
                task += j["plain_text"]
            results["Westcon"].append(task)

        pprint(results)

        return results

    def info_product_name(self, page_id):
        response = self.fetch_page(page_id)
        data = response.json()

        name = ""
        for i in data["properties"]["Name"]["title"]:
            name += i["plain_text"]

        return name

    def get_product(self):

        if not self.database_id:
            raise Exception("No database ID could be found.")

        response = self.fetch_database(
            database_id=self.database_id,
            json_filter={
                "filter": {
                    "and": [
                        {"property": "📚 Product", "relation": {"is_not_empty": True}},
                        {
                            "property": "🙋\u200d♂️ Customer",
                            "relation": {"is_empty": True},
                        },
                    ]
                }
            },
        )

        datas = response.json()

        results = {}

        for i in datas["results"]:
            customer_id = i["properties"]["📚 Product"]["relation"][0]["id"]
            customer_name = self.info_customer_name(customer_id)

            if customer_name not in results.keys():
                results[customer_name] = []

            task = ""
            for j in i["properties"]["Name"]["title"]:
                task += j["plain_text"]
            results[customer_name].append(task)

        pprint(results)

        return results

    def info_customer_name(self, page_id):
        response = self.fetch_page(page_id)
        data = response.json()

        name = ""
        for i in data["properties"]["Name"]["title"]:
            name += i["plain_text"]

        return name

    def get_customer(self):

        if not self.database_id:
            raise Exception("No database ID could be found.")

        response = self.fetch_database(
            database_id=self.database_id,
            json_filter={
                "filter": {
                    "and": [
                        {"property": "📚 Product", "relation": {"is_empty": True}},
                        {
                            "property": "🙋\u200d♂️ Customer",
                            "relation": {"is_not_empty": True},
                        },
                    ]
                }
            },
        )

        datas = response.json()

        results = {}

        for i in datas["results"]:
            customer_id = i["properties"]["🙋\u200d♂️ Customer"]["relation"][0]["id"]
            customer_name = self.info_customer_name(customer_id)

            if customer_name not in results.keys():
                results[customer_name] = []

            task = ""
            for j in i["properties"]["Name"]["title"]:
                task += j["plain_text"]
            results[customer_name].append(task)

        pprint(results)

        return results
