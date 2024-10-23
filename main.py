from json import JSONDecodeError
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Is called on "Generate Password"-button click
def generate_pw():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # selects characters from the lists above
    letter_list = [choice(letters) for _ in range(0, randint(7,10))]
    symbol_list = [choice(symbols) for _ in range(0, randint(2,4))]
    number_list = [choice(numbers) for _ in range(0, randint(2,4))]
    # combine into a password_list
    password_list = letter_list + symbol_list + number_list
    # gives the entries a random order (so you don´t get all letters first, etc.)
    shuffle(password_list)
    # turn password_list into string
    password = "".join(password_list)

    # put it into the entry box
    password_entry.insert(0, password)
    # copy it to the clipboard
    pyperclip.copy(password)

    messagebox.showinfo(title="PW", message="Password copied to clipboard.")

# ---------------------------- SAVE PASSWORD ------------------------------- #
#Is called on "Add"-button click
def save_password():
    #check all Entries
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data ={website: {"e-mail": email, "password":password}}

    #check if entry is empty
    if not len(password) or not len(email) or not len(website):
        messagebox.showinfo(title="Empty Fields", message="Don´t leave any fields empty")
    else:
        #show messagebox with info to be saved and ask for confirmation
        is_okay = messagebox.askyesno(title=website, message=f"These are the details entered:\nEmail: {email} "
                                                             f"\nPassword: {password}\nDo you want to save?")

        if is_okay :
            try:
                with open("passwords.json", "r") as f:
                    data = json.load(f)
                    data.update(new_data)
            except (FileNotFoundError, JSONDecodeError):
                with open("passwords.json", "w") as f:
                    json.dump(new_data, f, indent = 4)
            else:
                with open("passwords.json", "w") as f:
                    json.dump(data, f, indent = 4)
            finally:
                #show confirmation
                messagebox.showinfo(title="Password Saved", message="Password Saved")
                #clear password and website entry
                website_entry.delete(0,END)
                password_entry.delete(0,END)

# ---------------------------- LOOK UP PASSWORD ------------------------------- #
def search_pw():
    key = website_entry.get()
    try:
        with open("passwords.json","r") as f:
            data = json.load(f)
            try:
                messagebox.showinfo(f"{key}", f"E-mail: {data[key]["e-mail"]}\nPassword: {data[key]["password"]}")

            except KeyError:
                messagebox.showinfo("No Match","There is no password for the searched website, yet.")
    except FileNotFoundError:
        messagebox.showinfo("No File","There is no password file, yet.")

    except JSONDecodeError:
        messagebox.showinfo("No File", "There is no password stored, yet.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx= 20, pady = 20)

##### Canvas with Logo
canvas = Canvas()
canvas.config(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100,100, image=logo)
canvas.grid(row = 0,column = 1)

##### LABELS
website_label = Label(text="Website:")
website_label.grid(row = 1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row = 2, column=0)
password_label = Label(text="Password:")
password_label.grid(row = 3, column=0)

##### ENTRIES
website_entry = Entry(width=35)
website_entry.grid(row = 1, column = 1, columnspan=2, sticky= "W")
website_entry.focus() #put the cursor into the website entry

email_entry = Entry(width=35)
email_entry.grid(row = 2, column = 1, columnspan=2, sticky= "W")
# adding a default value to the E-mail field
# ***add your E-mail address here***
email_entry.insert(0,"Email@email.com")

password_entry = Entry(width= 21)
password_entry.grid(row = 3, column = 1, sticky = "W")

#### BUTTONS
generate_button = Button(text="Generate Password", command=generate_pw)
generate_button.grid(row = 3, column = 2, sticky= "W")

add_button = Button(text="Add", width=36, command= save_password)
add_button.grid(row = 4, column = 1, columnspan = 2, sticky= "W")

search_button = Button(text = "Search", command=search_pw)
search_button.grid(row = 1, column = 2, sticky= "W")




window.mainloop()