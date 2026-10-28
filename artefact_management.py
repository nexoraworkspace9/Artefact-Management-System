
VALID_CONDITIONS = ("Good", "Damage", "Under Repair")


def display_menu():
    print("\n" + "=" * 45)
    print("LOCAL HERITAGE COMMUNITY")
    print("ARTEFACT MANAGEMENT SYSTEM")
    print("=" * 45)
    print("1. Add New Artefact")
    print("2. View All Artefacts")
    print("3. Search Artefact")
    print("4. Update Artefact Condition")
    print("5. Exit")
    print("=" * 45)


def get_required_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: This field cannot be empty.")


def get_condition():
    while True:
        print("\nAvailable conditions:")
        for number, condition in enumerate(VALID_CONDITIONS, start=1):
            print(f"{number}. {condition}")

        choice = input("Select condition (1-3): ").strip()

        if choice in ("1", "2", "3"):
            return VALID_CONDITIONS[int(choice) - 1]

        print("Error: Please enter 1, 2 or 3.")


def generate_artefact_id(artefacts):
    highest_id = 0

    for artefact in artefacts:
        number = int(artefact["id"][1:])
        highest_id = max(highest_id, number)

    return f"A{highest_id + 1:03d}"


def add_artefact(artefacts):
    print("\n--- ADD NEW ARTEFACT ---")

    name = get_required_input("Enter artefact name: ")
    category = get_required_input("Enter category: ")
    location = get_required_input("Enter display location: ")
    condition = get_condition()

    artefact = {
        "id": generate_artefact_id(artefacts),
        "name": name,
        "category": category,
        "location": location,
        "condition": condition
    }

    artefacts.append(artefact)

    print("\nArtefact added successfully!")
    display_artefact(artefact)

    return artefact


def display_artefact(artefact):
    print("-" * 45)
    print(f"Artefact ID : {artefact['id']}")
    print(f"Name        : {artefact['name']}")
    print(f"Category    : {artefact['category']}")
    print(f"Location    : {artefact['location']}")
    print(f"Condition   : {artefact['condition']}")
    print("-" * 45)


def view_artefacts(artefacts):
    print("\n--- ALL ARTEFACTS ---")

    if not artefacts:
        print("No artefacts are currently available.")
        return

    print(f"Total artefacts: {len(artefacts)}")

    for artefact in artefacts:
        display_artefact(artefact)


def find_artefacts(artefacts, search_term):
    search_term = search_term.strip().casefold()

    if not search_term:
        return []

    return [
        artefact
        for artefact in artefacts
        if search_term in artefact["name"].casefold()
    ]


def search_artefact(artefacts):
    print("\n--- SEARCH ARTEFACT ---")

    if not artefacts:
        print("No artefacts are available to search.")
        return []

    search_term = get_required_input("Enter artefact name to search: ")
    matches = find_artefacts(artefacts, search_term)

    if not matches:
        print("No matching artefact found.")
        return []

    print(f"\n{len(matches)} matching artefact(s) found.")

    for artefact in matches:
        display_artefact(artefact)

    return matches


def find_artefact_by_id(artefacts, artefact_id):
    artefact_id = artefact_id.strip().upper()

    for artefact in artefacts:
        if artefact["id"].upper() == artefact_id:
            return artefact

    return None


def update_condition(artefacts):
    print("\n--- UPDATE ARTEFACT CONDITION ---")

    if not artefacts:
        print("No artefacts are available to update.")
        return False

    artefact_id = get_required_input("Enter artefact ID: ")
    artefact = find_artefact_by_id(artefacts, artefact_id)

    if artefact is None:
        print("Error: Artefact ID not found.")
        return False

    print("\nSelected artefact:")
    display_artefact(artefact)

    old_condition = artefact["condition"]
    new_condition = get_condition()

    artefact["condition"] = new_condition

    print("\nArtefact condition updated successfully!")
    print(f"Previous condition: {old_condition}")
    print(f"Updated condition : {new_condition}")

    return True


def main():
    artefacts = []

    print("Welcome to Local Heritage Community")

    while True:
        display_menu()

        try:
            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                add_artefact(artefacts)

            elif choice == "2":
                view_artefacts(artefacts)

            elif choice == "3":
                search_artefact(artefacts)

            elif choice == "4":
                update_condition(artefacts)

            elif choice == "5":
                print("\nThank you for using the Artefact Management System.")
                print("Goodbye!")
                break

            else:
                print("\nInvalid choice. Please select a number from 1 to 5.")

        except (EOFError, KeyboardInterrupt):
            print("\nProgram terminated by user.")
            break


if __name__ == "__main__":
    main()
