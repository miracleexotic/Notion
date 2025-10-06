from dotenv import dotenv_values
from src.Notion import Month, Food, Todo, Transport, Wash


if __name__ == "__main__":

    config = dotenv_values(".env.secret")

    food = Food(config["BEARER_TOKEN"])
    transport = Transport(config["BEARER_TOKEN"])
    wash = Wash(config["BEARER_TOKEN"])

    start_date = "2025-09-01"
    end_date = "2025-09-30"
    file_ttb = "data/AccountStatement_30092025.pdf"

    # food.create_by_date(start_date, end_date, file_ttb)
    # transport.create_by_date(start_date, end_date, file_ttb)
    # wash.create_by_date(start_date, end_date)

    # food.update_by_date(start_date, end_date)
    # transport.update_by_date(start_date, end_date)

    # month = Month(config['BEARER_TOKEN'])
    # month.get_by_date("2024-09-01")

    # todo = Todo(config['BEARER_TOKEN'])
    # todo.get_westcon()
    # print('---')
    # todo.get_product()
    # print('---')
    # todo.get_customer()
