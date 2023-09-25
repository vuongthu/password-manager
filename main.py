from tkinter import *
# Since messagebox is not a class, it is not imported from Line 1
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

FONT = ("Arial", 12, "normal")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = ''.join(password_list)
    password_entry.insert(0, password)
    # Once you hit generate password, you want it to save it onto the clipboard without needing to copy/paste
    # We do this with the pyperclip module
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = user_email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Uh Oh!", message="Please do not leave any fields empty!")
    else:

        # Standard Dialogs are pop-ups that Tkinter can generate
        # Message boxes are easy to create - just tap into the module
        # messagebox.showinfo(title="Title", message="Message")
        # We can also ask the user something
        # is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
        #                                               f"\nPassword: {password} \nIs it ok to save?")

        # Commented the is_ok check out to work on Day 30, JSON file
        # If we don't have the data initially, then it would be difficult to update it
        # We need to work on exceptions!
        # It will show FileNotFoundError since there is nothing in the data.json file

        # if is_ok:
        try:
            with open("data.json", mode="r") as data_file:
                # How to Read in JSON, make sure mode is "r"
                # Reading the Old Data
                data = json.load(data_file)
                # print(data)  # Load takes the data and converts it into a python dictionary
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # How to Write in JSON, make sure mode is "w"
                # We moved it to the end of this sequence because we want it to write the new data
                json.dump(new_data, data_file, indent=4)
        else:
            # How to Update data in JSON, we don't want to override the file
            # Updating Old Data with New Data
            data.update(new_data)
            # We want to open up the data again in write mode

            with open("data.json", mode="w") as data_file:
                # How to Write in JSON, make sure mode is "w"
                # We moved it to the end of this sequence because we want it to write the new data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD THROUGH SEARCH ------------------------------- #

def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website.title() in data:
            email = data[website]["email"]
            password = data[website]["password"]

            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Uh oh!", message="No details for the website exists.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="black")

canvas = Canvas(width=200, height=200, bg="black", highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", font=FONT, bg="black", fg="white")
website_label.grid(column=0, row=1)
user_email_label = Label(text="Username/Email:", font=FONT, bg="black", fg="white")
user_email_label.grid(column=0, row=2)
password_label = Label(text="Password:", font=FONT, bg="black", fg="white")
password_label.grid(column=0, row=3)

# Entry
# Updated website entry width from 52 to 33, removed column span in grid to accommodate for search button
website_entry = Entry(width=33, bg="black", fg="white")
website_entry.grid(column=1, row=1)
website_entry.focus()
user_email_entry = Entry(width=52, bg="black", fg="white")
user_email_entry.grid(column=1, row=2, columnspan=2)
# END is just a constant that represents the last character inside the entry box
user_email_entry.insert(END, "kelsi.vuong@yahoo.com")
password_entry = Entry(width=33, bg="black", fg="white")
password_entry.grid(column=1, row=3)

# Buttons
gen_pass_button = Button(text="Generate Password", width=14, bg="grey", fg="white", command=generate_password)
gen_pass_button.grid(column=2, row=3)
add_button = Button(text="Add", width=44, bg="grey", fg="white", command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=14, bg="grey", fg="white", command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
