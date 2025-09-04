from src.Notion.Base.notion import Notion


class Work(Notion):

    def __init__(self, bearer_token):
        super().__init__(bearer_token)

    def __str__(self):
        db_id = "".join(
            [
                f"\n\t- {k.split('WORK_')[1]}: {v}"
                for k, v in self.env.items()
                if k.startswith("WORK_")
            ]
        )
        return f"Database id [{__class__.__name__}]: {db_id}"
