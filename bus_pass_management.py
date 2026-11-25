# Bus Pass Management System
# Python 3 | Lists, Dictionaries, Functions, File Handling

PASS_TYPES = {
    "Monthly": {"days": 30, "fee": 500},
    "Quarterly": {"days": 90, "fee": 1350},
    "Yearly": {"days": 365, "fee": 4800},
}
CATEGORIES = ("General", "Student")
DATA_FILE = "buspass.txt"


def load_passes():
    """Load saved passes from the text file."""
    passes = []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.rstrip("\n").split("|")
                if len(parts) != 7:
                    continue
                pass_id, name, route, pass_type, category, fee, days = parts
                try:
                    passes.append({
                        "id": pass_id,
                        "name": name,
                        "route": route,
                        "type": pass_type,
                        "category": category,
                        "fee": int(fee),
                        "days": int(days),
                    })
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return passes


def save_passes(passes):
    """Save all passes; one pass is stored on each line."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        for p in passes:
            file.write(
                f'{p["id"]}|{p["name"]}|{p["route"]}|{p["type"]}|'
                f'{p["category"]}|{p["fee"]}|{p["days"]}\n'
            )


def next_pass_id(passes):
    """Generate BP101 for the first pass, then the next available ID."""
    numbers = []
    for p in passes:
        try:
            numbers.append(int(p["id"][2:]))
        except (ValueError, TypeError):
            continue
    return f"BP{max(numbers, default=100) + 1:03d}"


def calculate_fee(pass_type, category):
    base_fee = PASS_TYPES[pass_type]["fee"]
    return int(base_fee * 0.75) if category == "Student" else base_fee


def display_pass(p):
    print(
        f'{p["id"]} | {p["name"]} | {p["route"]} | {p["type"]} | '
        f'{p["category"]} | Fee: Rs. {p["fee"]} | Valid: {p["days"]} days'
    )


def issue_pass(passes):
    print("\n--- Issue New Pass ---")
    name = input("Name: ").strip()
    route = input("Route: ").strip()
    pass_type = input("Type (Monthly/Quarterly/Yearly): ").strip().title()
    category = input("Category (General/Student): ").strip().title()

    if not name or not route:
        print("Name and route cannot be empty. Pass not issued.")
        return
    if pass_type not in PASS_TYPES:
        print("Invalid pass type. Choose Monthly, Quarterly or Yearly. Pass not issued.")
        return
    if category not in CATEGORIES:
        print("Invalid category. Choose General or Student. Pass not issued.")
        return

    fee = calculate_fee(pass_type, category)
    p = {
        "id": next_pass_id(passes),
        "name": name,
        "route": route,
        "type": pass_type,
        "category": category,
        "fee": fee,
        "days": PASS_TYPES[pass_type]["days"],
    }
    passes.append(p)
    save_passes(passes)
    print(
        f'Pass issued. ID: {p["id"]} | {name} | {route} | {pass_type} | '
        f'Fee: Rs. {fee} | Valid: {p["days"]} days'
    )


def renew_pass(passes):
    print("\n--- Renew Existing Pass ---")
    pass_id = input("Enter pass ID: ").strip().upper()
    for p in passes:
        if p["id"].upper() == pass_id:
            # Renewal keeps the existing pass type and category.
            p["fee"] = calculate_fee(p["type"], p["category"])
            p["days"] = PASS_TYPES[p["type"]]["days"]
            save_passes(passes)
            print("Pass renewed successfully:")
            display_pass(p)
            return
    print("Pass ID not found. Pass not renewed.")


def search_pass(passes):
    print("\n--- Search Pass ---")
    pass_id = input("Enter pass ID: ").strip().upper()
    for p in passes:
        if p["id"].upper() == pass_id:
            display_pass(p)
            return
    print("Pass not found.")


def view_all_passes(passes):
    print("\n--- All Bus Passes ---")
    if not passes:
        print("No passes issued yet.")
        return
    for p in passes:
        display_pass(p)


def main():
    passes = load_passes()
    while True:
        print("\n===== BUS PASS MANAGEMENT SYSTEM =====")
        print("1. Issue New Pass")
        print("2. Renew Existing Pass")
        print("3. Search Pass by ID")
        print("4. View All Passes")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            issue_pass(passes)
        elif choice == "2":
            renew_pass(passes)
        elif choice == "3":
            search_pass(passes)
        elif choice == "4":
            view_all_passes(passes)
        elif choice == "5":
            print("Thank you for using Bus Pass Management System.")
            break
        else:
            print("Invalid menu choice. Please enter 1 to 5.")


if __name__ == "__main__":
    main()
