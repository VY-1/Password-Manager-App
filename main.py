from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)


    letters_list = [random.choice(letters) for _ in range(nr_letters)]
    numbers_list = [random.choice(numbers) for _ in range(nr_symbols)]
    symbols_list = [random.choice(symbols) for _ in range(nr_numbers)]
    password_list = letters_list + numbers_list + symbols_list

    random.shuffle(password_list)

    password = "".join(password_list)

    # password = ""
    # for char in password_list:
    #   password += char

    #print(f"Your password is: {password}")
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ------------------------------- SEARCH ----------------------------------- #
def get_login_info():
    website = website_entry.get()
    try:

        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No database file found, add a record to create one")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            #Clear email and password entries
            email_entry.delete(0, END)
            password_entry.delete(0, END)

            #Load email and password from data.json to email and password entry fields
            email_entry.insert(0, email)
            password_entry.insert(0, password)
            messagebox.showinfo(title=website, message=f"Email/Username: {email} \nPassword: {password}")
        else:
            messagebox.showinfo(message="No login entry found for Website")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data= {
        website: {
            "email": email,
            "password": password

        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Invalid inputs!", message="Please don't leave any filed empty!")

    else:

        try:
            with open("data.json", "r") as data_file:

                #Reading old data
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:

            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:

                #Saving updated data
                json.dump(data, data_file, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

#Label
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

#Entry
website_entry = Entry(width=30)
website_entry.grid(sticky=W, row=1, column=1)
website_entry.focus()   #start of with the cursor in the website_entry field

email_entry = Entry(width=30)
email_entry.grid(sticky=W, row=2, column=1)
email_entry.insert(0, "username@domain.com")

password_entry = Entry(width=30)
password_entry.grid(sticky=W, row=3, column=1)

#Button
search_button = Button(text="Search", width=15, command=get_login_info)
search_button.grid(sticky=W, row=1, column=2)

password_button = Button(text="Generate Password", width=15, command=generate_password)
password_button.grid(sticky=W, row=3, column=2)

add_button = Button(text="Add/Update", width=15, command=save)
add_button.grid(sticky=W, row=4, column=2)



window.mainloop()