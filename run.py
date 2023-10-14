import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

sales = SHEET.worksheet("sales")

def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            break

    return sales_data

def validate_data(values):
    """
    Validate entered data
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"Exactly 6 values required, you provided  {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True

def update_sales_worksheet(data):
    """
    Update sales worksheet
    """
    print("Updating sales worksheet...\n")
    sales_workheet = SHEET.worksheet("sales")
    sales_workheet.append_row(data)
    print("Sales worksheet updated successfully\n")

def calculate_surplus_data(sales_row):
    print("Calculating surplus data...")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)

def main():
    """
    Run all functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

print("Welcome to Love Sandwiches Data Automation")
main()