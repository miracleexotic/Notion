from src.Notion.Base.notion import Notion


class Finance(Notion):

    def __init__(self, bearer_token):
        super().__init__(bearer_token)

    def __str__(self):
        db_id = "".join(
            [
                f"\n\t- {k.split('FINANCE_')[1]}: {v}"
                for k, v in self.env.items()
                if k.startswith("FINANCE_")
            ]
        )
        return f"Database id [{__class__.__name__}]: {db_id}"
