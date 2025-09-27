import argparse
from .utils import create_session
from .client import NetSuiteClient
from . import config


def print_employee(emp):
    if not emp:
        print("❌ Could not retrieve employee record.")
        return
    print("\n/---------- Employee Details -----/")
    print(f" Internal ID: {emp.get('id', 'N/A')}")
    print(f" Entity ID: {emp.get('entityId', 'N/A')}")
    print(f" Name (Raw): {emp.get('displayName', 'N/A')}")
    print(f" Email: {emp.get('email', 'N/A')}")
    print(f" Title: {emp.get('title', 'N/A')}")
    dept = emp.get('department', {})
    print(f" Department: {dept.get('refName', 'N/A')} (ID: {dept.get('id', 'N/A')})")
    print(f" Is Inactive: {emp.get('isInactive', 'N/A')}")
    print("/---------------------------------/\n")


def main():
    parser = argparse.ArgumentParser(description="Fetch employee details from NetSuite.")
    parser.add_argument("employee_id", nargs="?", type=int, default=1662,
                        help="Internal ID of the employee (default: 1662)")
    args = parser.parse_args()

    session = create_session()
    client = NetSuiteClient(session)
    client.auth.load_refresh_token()

    if not client.auth.refresh_token and not config.REDIRECT_URI:
        print("🌐 First-time setup required. Open this URL:\n", client.auth.get_authorize_url())
    else:
        if client.test_connection():
            emp = client.get_employee(args.employee_id)
            print_employee(emp)


if __name__ == "__main__":
    main()
