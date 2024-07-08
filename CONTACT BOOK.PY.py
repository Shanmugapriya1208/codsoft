import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store the contacts
CONTACTS_FILE = 'contacts.json'

# Function to load contacts from the file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    return []

# Function to save contacts to the file
def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)

# Main application class
class ContactApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contact Manager")
        self.geometry("500x500")
        self.contacts = load_contacts()
        
        self.create_widgets()
        self.display_contacts()

    def create_widgets(self):
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self, width=50)
        self.name_entry.pack(pady=5)

        self.phone_label = tk.Label(self, text="Phone:")
        self.phone_label.pack(pady=5)
        self.phone_entry = tk.Entry(self, width=50)
        self.phone_entry.pack(pady=5)

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self, width=50)
        self.email_entry.pack(pady=5)

        self.address_label = tk.Label(self, text="Address:")
        self.address_label.pack(pady=5)
        self.address_entry = tk.Entry(self, width=50)
        self.address_entry.pack(pady=5)

        self.add_button = tk.Button(self, text="Add Contact", command=self.add_contact)
        self.add_button.pack(pady=10)

        self.contacts_listbox = tk.Listbox(self, width=80, height=15)
        self.contacts_listbox.pack(pady=10)
        
        self.update_button = tk.Button(self, text="Update Contact", command=self.update_contact)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(self, text="Delete Contact", command=self.delete_contact)
        self.delete_button.pack(pady=5)

        self.search_label = tk.Label(self, text="Search by Name or Phone:")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self, width=50)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self, text="Search", command=self.search_contact)
        self.search_button.pack(pady=5)

    def display_contacts(self):
        self.contacts_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contacts_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()
        if name and phone:
            self.contacts.append({"name": name, "phone": phone, "email": email, "address": address})
            save_contacts(self.contacts)
            self.display_contacts()
            self.clear_entries()
        else:
            messagebox.showwarning("Warning", "Name and Phone are required")

    def update_contact(self):
        try:
            selected_index = self.contacts_listbox.curselection()[0]
            self.contacts[selected_index] = {
                "name": self.name_entry.get().strip(),
                "phone": self.phone_entry.get().strip(),
                "email": self.email_entry.get().strip(),
                "address": self.address_entry.get().strip()
            }
            save_contacts(self.contacts)
            self.display_contacts()
            self.clear_entries()
        except IndexError:
            messagebox.showwarning("Warning", "No contact selected")

    def delete_contact(self):
        try:
            selected_index = self.contacts_listbox.curselection()[0]
            self.contacts.pop(selected_index)
            save_contacts(self.contacts)
            self.display_contacts()
        except IndexError:
            messagebox.showwarning("Warning", "No contact selected")

    def search_contact(self):
        search_term = self.search_entry.get().strip().lower()
        matching_contacts = [
            contact for contact in self.contacts 
            if search_term in contact['name'].lower() or search_term in contact['phone']
        ]
        self.contacts_listbox.delete(0, tk.END)
        for contact in matching_contacts:
            self.contacts_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

if __name__ == '__main__':
    app = ContactApp()
    app.mainloop()
