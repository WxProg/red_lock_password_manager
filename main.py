import pyperclip
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json

generate_button_counter = 0
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    global generate_button_counter
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter =  [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letter + password_symbols + password_numbers

    shuffle(password_list)

    final_password = "".join(password_list)
    password_entry.insert(0, final_password)
    # A modules that copies to windows clipboard by calling the method below
    pyperclip.copy(final_password)
    generate_button_counter += 1
    if generate_button_counter > 1:
        password_entry.delete(0, END)
        password_entry.insert(0, final_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website_entry = web_entry.get()
    em_us_entry = email_entry.get()
    pass_entry = password_entry.get()
    new_data = {
        website_entry:{
            "email": em_us_entry,
            "password": pass_entry,
        }
    }

    if website_entry == "" or pass_entry == "":
        messagebox.showwarning(title="Warning!", message="All fields are required.")
    else:
        try:
            with open("data.json", "r") as pw_data:
                # Reading old data
                data = json.load(pw_data)
        except FileNotFoundError:
            with open("data.json", "w") as pw_data:
                json.dump(new_data, pw_data, indent=2 )
        else:
            # Updating the old data with new data
            data.update(new_data)
            with open("data.json", "w") as pw_data:
                # writing and saving the updated data
                json.dump(data, pw_data, indent=2)
        finally:
            web_entry.delete(0, END)
            password_entry.delete(0, END)
# ---------------------------- SEARCH ------------------------------- #

def find_password():
    website_search = web_entry.get()
    try:
        with open("data.json", "r") as pw_data:
            web_dict = json.load(pw_data)
    except FileNotFoundError:
        messagebox.showwarning(title="ERROR", message="No Data File Found")
    else:
        if website_search in web_dict:
            messagebox.showinfo(title=website_search.title(), message=f"Email: {web_dict[website_search]['email']}\n"
                                                              f"Password: {web_dict[website_search]['password']}")
        else:
            messagebox.showwarning(title="Invalid Website", message=f" Website: {website_search} not in data file.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Red Lock Password Manager")
window.config(padx=50, pady=50)

#Creating the canvas with the padlock logo
pw_man_canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
pw_man_canvas.create_image(100, 100, image= lock_img)
pw_man_canvas.grid(row=0,column=1)

website = Label(text="Website: ", font=("sans serif", 14, "normal"))
website.grid(row=1, column=0)
web_entry = Entry(width=32)
web_entry.grid(row=1, column=1)
web_entry.focus()
email_username = Label(text="Email/Username:", font=("sans serif", 14, "normal"))
email_username.grid(row=2, column=0)
email_entry = Entry(width=51)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "chadmysta18@gmail.com")

password = Label(text="Password:", font=("sans serif", 14, "normal"))
password.grid(row=3, column=0)
password_entry = Entry(width=32)
password_entry.grid(row=3, column=1)

generate = Button(text="Generate Password", command=generate_password)
generate.grid(row=3, column=2)

add = Button(text="Add", width=43, command=save)
add.grid(row=4, column=1, columnspan=2)

search = Button(text="Search", width=14, command=find_password)
search.grid(row=1, column=2)

window.mainloop()