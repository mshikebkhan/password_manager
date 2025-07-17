from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
from pyperclip import copy
import os
import json

# ? Use Documents folder (always writable by user)
json_file_path = os.path.join(os.path.expanduser("~"), "Documents", "locker.json")

# ---- PASSWORD FINDER ---- #
def search_password():
    website = website_entry.get()
    if website != "":
        try:
            with open(json_file_path, 'r') as locker_file:
                data = json.load(locker_file)
                try:
                    data_dict = data[website]
                except KeyError:
                    messagebox.showerror(title="Oops!", message="Password does not found for this website.")
                else:
                    messagebox.showinfo(title=website, message=f"Username/Emaiil: {data_dict['username']}\n"
                                                               f"Password: {data_dict['password']}")
        except FileNotFoundError:
            messagebox.showerror(title="Oops!", message="Database file not found.")

# ---- PASSWORD GENERATOR ---- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_count = 3
    numbers_count = 3
    symbols_count = 3

    password = ""

    # Pick N Letters
    for letter in range(1, letters_count+1):
        rn = randint(0, 50)
        password += letters[rn]

    # Pick N Numbers
    for number in range(1, numbers_count+1):
        password += choice(numbers)

    # Pick N Symbols
    for symbol in range(1, symbols_count+1):
        password += choice(symbols)

    # Print Shuffled password
    password_list = list(password)
    shuffle(password_list)
    final_password = ""
    final_password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, final_password)
    copy(password)

    messagebox.showinfo(title="Done!", message="Password copied to clipboard.")

# ---- SAVE PASSWORD ---- #
def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": password
        }
    }

    if website == "" or username == "" or password == "":
        messagebox.showerror(title="Oops!", message="Please fill all the fields.")
    else:
        messagebox.askokcancel(title=website, message=f"Verify your details you entered:\n"
                                                      f"Username/Email: {username}\n"
                                                      f"Password: {password}\n"
                                                      f"Should we proceed?")

        try:
            locker_file = open(json_file_path, "r") # Check if file exists.
            data = json.load(locker_file)  # Reading old data.
            data.update(new_data)  # Updating old data.
            locker_file.close()
        except FileNotFoundError: # Create a brand new file with new data :)
            locker_file = open(json_file_path, "w")
            json.dump(new_data, locker_file, indent=4)
            locker_file.close()
        else:
            locker_file = open(json_file_path, "w") # Writing updated data.
            json.dump(data, locker_file, indent=4)
            locker_file.close()
        finally:
            website_entry.delete(0, END)
            username_entry.delete(0, END)
            password_entry.delete(0, END)



# ---- UI SETUP ---- #
window = Tk()
window.title("Password Manager")
window.iconbitmap("lock.ico")
window.config(padx=50, pady=50)

canvas = Canvas(height=220, width=200)
lock_img = PhotoImage(file="lock.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
username_label = Label(text="Username/Email:")
username_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=39)
website_entry.grid(column=1, row=1)
website_entry.focus()
username_entry = Entry(width=60)
username_entry.grid(column=1, row=2, columnspan=2)
# username_entry.insert(0, "mshikebkhan@gmail.com")
password_entry = Entry(width=39)
password_entry.grid(column=1, row=3)

# Buttons
search_btn = Button(text="Search", width=14, background="red", foreground="white", command=search_password)
search_btn.grid(column=2, row=1, pady=5)
generate_pass_btn = Button(text="Generate Password", background="green", foreground="white", command=generate_password)
generate_pass_btn.grid(column=2, row=3, pady=5)
add_btn = Button(text="Add", width=51, background="blue", foreground="white", command=save)
add_btn.grid(column=1, row=4, columnspan=2, pady=2)
add_btn.config(pady=5)

window.mainloop()
