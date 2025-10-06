from datetime import datetime, date
from pprint import pprint
import camelot
import pandas as pd
import numpy as np


def extract_TTB_pdf(filepath):
    tables = camelot.read_pdf(filepath=filepath, flavor="stream", pages="all")

    combined_df: pd.DataFrame = pd.DataFrame()

    for t in tables[1:]:
        df = t.df

        # Set 1st row as header
        df.columns = df.iloc[0].tolist()
        df = df.drop(df.index[0]).reset_index(drop=True)

        # Drop columns
        drop_columns = ["Time", "Transaction", "Channel", "Balance"]
        df = df.drop(columns=drop_columns)

        # Drop empty row
        df.replace("", np.nan, inplace=True)
        df = df.dropna()

        if not combined_df.empty:
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        else:
            combined_df = df

    items = combined_df.to_dict(
        orient="records",
    )
    items_by_date = {}
    for item in items:
        date_str = datetime.strptime(item["Date"], "%d %b %y").strftime("%Y-%m-%d")

        # Init data by date
        if date_str not in items_by_date.keys():
            items_by_date[date_str] = []

        # Append data
        items_by_date[date_str].append(
            {"Amount": item["Amount"], "Details": item["Details"]}
        )

    return items_by_date


def convert_amount(amount: str):
    multiply = 1.00 if amount.startswith("+") else -1.00
    total = float(amount.strip("+").strip("-").replace(",", "")) * multiply

    if total % 1 == 0:
        total = int(total)

    return total


def get_category(details: str):
    categories = {
        "LineMan": ["LINE MAN"],
        "TrueMoney": ["True Money"],
        "Traffic": ["MRT-", "BTS", "WWW.GRAB.COM"],
    }

    for category in categories.keys():
        for item in categories[category]:
            idx = details.find(item)
            if idx > -1:
                return category
    else:
        return "TTB"


def spend_food_data_format(data: list):
    lst = {"LineMan": [], "TrueMoney": [], "TTB": [], "Other": []}

    for item in data:
        amount = convert_amount(item["Amount"])
        if amount < 0:
            category = get_category(item["Details"])
            if category in ["LineMan", "TTB"]:
                lst[category].append(str(amount * -1))

    lst_str = f"LineMan({','.join(lst['LineMan'])}), TrueMoney({','.join(lst['TrueMoney'])}), TTB({','.join(lst['TTB'])}), Other({','.join(lst['Other'])})"
    return lst_str


def spend_traffic_data_format(data: list):
    lst = []

    for item in data:
        amount = convert_amount(item["Amount"])
        if amount < 0:
            category = get_category(item["Details"])
            if category in ["Traffic"]:
                lst.append(str(amount * -1))

    lst_str = ",".join(lst)
    return lst_str


if __name__ == "__main__":
    items_by_date = extract_TTB_pdf("data/AccountStatement_30092025.pdf")

    start_date = "2025-09-01"
    end_date = "2025-09-30"

    sdate = date(*list(map(int, start_date.split("-"))))
    edate = date(*list(map(int, end_date.split("-"))))
    date_ranges = pd.date_range(sdate, edate, freq="d").to_list()
    date_ranges = list(map(lambda x: x.strftime("%Y-%m-%d"), date_ranges))

    for date_day in date_ranges:
        print(date_day)
        print(spend_food_data_format(items_by_date[date_day]))
        print(spend_traffic_data_format(items_by_date[date_day]))
