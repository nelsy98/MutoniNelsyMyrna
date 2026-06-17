import re


class ContactManager:
    def __init__(self):
        self.contacts = []   
        self._next_id = 1

    def _valid_phone(self, phone):
        return bool(re.fullmatch(r'[+\d][\d\-]*', phone))

    def _valid_email(self, email):
        if not email:
            return True
        return "@" in email and "." in email

    def _find(self, contact_id):
        for c in self.contacts:
            if c["id"] == contact_id:
                return c
        return None

    def add_contact(self, name, phone, email=None):
        if not self._valid_phone(phone):
            print(f"Error: '{phone}' is invalid. Use only digits and hyphens.")
            return
        if not self._valid_email(email):
            print(f"Error: '{email}' is not a valid email. It must contain '@' and '.'.")
            return
        self.contacts.append({
            "id"   : self._next_id,
            "name" : name,
            "phone": phone,
            "email": email,
        })
        print(f"Contact '{name}' added (ID {self._next_id}).")
        self._next_id += 1

    def view_contact(self, contact_id):
        c = self._find(contact_id)
        if c:
            self._print_contact(c)
        else:
            print(f"No contact found with ID {contact_id}.")

    def update_contact(self, contact_id, name=None, phone=None, email=None):
        c = self._find(contact_id)
        if not c:
            print(f"No contact found with ID {contact_id}.")
            return
        new_phone = phone if phone else c["phone"]
        new_email = email if email is not None else c["email"]
        if not self._valid_phone(new_phone):
            print(f"Error: '{new_phone}' is invalid.")
            return
        if not self._valid_email(new_email):
            print(f"Error: '{new_email}' is not a valid email.")
            return
        if name:  c["name"]  = name
        c["phone"] = new_phone
        c["email"] = new_email
        print(f"Contact ID {contact_id} updated.")

    def delete_contact(self, contact_id):
        c = self._find(contact_id)
        if c:
            self.contacts.remove(c)
            print(f"Contact ID {contact_id} deleted.")
        else:
            print(f"No contact found with ID {contact_id}.")

    def search_contacts(self, query):
        q = query.lower()
        results = [
            c for c in self.contacts
            if q in c["name"].lower()
            or q in c["phone"]
            or q in (c["email"] or "").lower()
        ]
        if not results:
            print(f"No contacts matched '{query}'.")
            return
        print(f"\nSearch results for '{query}' ({len(results)} found):")
        print("-" * 45)
        for c in results:
            self._print_contact(c)

    def list_all_contacts(self):
        if not self.contacts:
            print("No contacts saved yet.")
            return
        sorted_contacts = sorted(self.contacts, key=lambda c: c["name"].lower())
        print(f"\nAll contacts ({len(sorted_contacts)} total):")
        print("-" * 45)
        for c in sorted_contacts:
            self._print_contact(c)

    def _print_contact(self, c):
        print(f"  ID   : {c['id']}")
        print(f"  Name : {c['name']}")
        print(f"  Phone: {c['phone']}")
        print(f"  Email: {c['email']}")
        print("-" * 45)


def main():
    manager = ContactManager()

    while True:
        print("""
              Contact Manager Menu
              1. Add Contact
              2. View Contact
              3. Update Contact
              4. Delete Contact
              5. Search Contacts
              6. List All Contacts
              7. Exit
              """
              )
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            name  = input("  Name  : ").strip()
            phone = input("  Phone : ").strip()
            email = input("  Email (press Enter to skip): ").strip() or None
            manager.add_contact(name, phone, email)

        elif choice == "2":
            contact_id = input("  Contact ID: ").strip()
            if contact_id.isdigit():
                manager.view_contact(int(contact_id))
            else:
                print("  Please enter a valid numeric ID.")

        elif choice == "3":
            contact_id = input("  Contact ID to update: ").strip()
            if not contact_id.isdigit():
                print("  Please enter a valid numeric ID.")
                continue
            print("  (Press Enter to keep the current value)")
            name  = input("  New name  : ").strip() or None
            phone = input("  New phone : ").strip() or None
            email = input("  New email : ").strip() or None
            manager.update_contact(int(contact_id), name, phone, email)

        elif choice == "4":
            contact_id = input("  Contact ID to delete: ").strip()
            if contact_id.isdigit():
                manager.delete_contact(int(contact_id))
            else:
                print("  Please enter a valid numeric ID.")

        elif choice == "5":
            query = input("  Search term: ").strip()
            manager.search_contacts(query)

        elif choice == "6":
            manager.list_all_contacts()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("  Invalid option. Please choose 1 to 7.")


if __name__ == "__main__":
    main()
