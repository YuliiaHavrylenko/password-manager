from tkinter import *
from tkinter import messagebox
import random
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    entry_password.delete(0, 'end')
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for i in range(nr_letters)] + [random.choice(numbers) for s in
                                                                           range(nr_symbols)] \
                    + [random.choice(symbols) for n in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)
    entry_password.insert(0, f"{password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    data_web = entry_website.get().capitalize()
    data_user = entry_user.get()
    data_password = entry_password.get()
    new_data = {
        data_web: {
            "email": data_user,
            "password": data_password,
        }
    }
    if len(data_web) == 0 or len(data_web) == 0 or data_password == 0:
        oops = messagebox.showinfo(title="Oops", message="Please don't leave fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            entry_website.delete(0, 'end')
            entry_password.delete(0, 'end')


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def find_password():
        try:
            with open("data.json", "r") as data_file:
                old_data = json.load(data_file)
                search_web = entry_website.get().capitalize()
                search_email = old_data[search_web]["email"]
                search_password = old_data[search_web]["password"]
                search_result = messagebox.showinfo(title="Search Result",
                                                    message=f"Email: {search_email} \n"
                                                            f"Password: {search_password}")
        except FileNotFoundError:
            search_result = messagebox.showinfo(title="No Data File Found",
                                                message="You dont have any data")
        except KeyError:
            search_result = messagebox.showinfo(title="No Data File Found",
                                                message="No details for the website exist")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# logo
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# label website
label_website = Label(text="Website:", font=("Helvetica", 12))
label_website.grid(row=1, column=0)

# label email/username
label_user = Label(text="Email/Username:", font=("Helvetica", 12))
label_user.grid(row=2, column=0)

# label password
label_password = Label(text="Password:", font=("Helvetica", 12))
label_password.grid(row=3, column=0)

# entry website
entry_website = Entry(width=30)
entry_website.focus()
entry_website.grid(row=1, column=1, columnspan=2)

# entry user
entry_user = Entry(width=30)
entry_user.grid(row=2, column=1, columnspan=2)
entry_user.insert(0, "example@gmail.com")

# entry password
entry_password = Entry(width=30)
entry_password.grid(row=3, column=1, columnspan=2)

# button generate password
button_generate = Button(text="Generate", command=generate_password, width=7)
button_generate.grid(row=3, column=3, padx=0, pady=0)

# button add to data
button_add = Button(text="Add", command=save, width=25)
button_add.grid(row=4, column=1, padx=0, pady=0)

# button search from data
button_search = Button(text="Search", command=find_password, width=7)
button_search.grid(row=1, column=3, padx=0, pady=0)

window.mainloop()
