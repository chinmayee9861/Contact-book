import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect('contacts2.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS contacts
             (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT)''')
conn.commit()


# Functions to handle database operations
def add_contact():
    name = entry_name.get().capitalize()
    phone = entry_phone.get()
    email = entry_email.get()

    if name and phone and email:
        c.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        conn.commit()
        messagebox.showinfo("Success", "Contact added successfully!")
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        view_contacts()
    else:
        messagebox.showwarning("Input error", "All fields are required")


def view_contacts():
    for row in tree.get_children():
        tree.delete(row)

    c.execute("SELECT * FROM contacts")
    rows = c.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)


def delete_contact():
    selected_item = tree.selection()
    if selected_item:
        contact_id = tree.item(selected_item)['values'][0]
        c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        messagebox.showinfo("Success", "Contact deleted successfully!")
        view_contacts()
    else:
        messagebox.showwarning("Selection error", "No contact selected")


# GUI setup
root = tk.Tk()
root.title("Contact Book")
root.geometry("400x400")

# Labels and entry fields
frame_form = tk.Frame(root, padx=10, pady=10)
frame_form.pack(fill=tk.X)

tk.Label(frame_form, text="Name").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_form)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Phone").grid(row=1, column=0, padx=5, pady=5)
entry_phone = tk.Entry(frame_form)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Email").grid(row=2, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_form)
entry_email.grid(row=2, column=1, padx=5, pady=5)

# Buttons
frame_buttons = tk.Frame(root, padx=10, pady=10)
frame_buttons.pack(fill=tk.X)

tk.Button(frame_buttons, text="Add Contact", command=add_contact).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(frame_buttons, text="Delete Contact", command=delete_contact).pack(side=tk.LEFT, padx=5, pady=5)

# Treeview for displaying contacts
frame_tree = tk.Frame(root, padx=10, pady=10)
frame_tree.pack(fill=tk.BOTH, expand=True)

columns = ('id', 'name', 'phone', 'email')
tree = ttk.Treeview(frame_tree, columns=columns, show='headings')
tree.heading('id', text='ID')
tree.heading('name', text='Name')
tree.heading('phone', text='Phone')
tree.heading('email', text='Email')

tree.pack(fill=tk.BOTH, expand=True)

# Initialize the view with existing contacts
view_contacts()

# Run the application
root.mainloop()

# Close the database connection
conn.close()