import tkinter
from tkinter import messagebox
import random
import pyperclip
import pandas
import os
import pandastable  #tkinder module for showing CSVs

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
GREY = "#8E8380"
WHITE = "#FFFFFF"
PASSWORD_PATH = '/Users/daniil.makhonia/Documents/100dofpython/day29/passwords.csv'

# trying to open a file. Otherwise, create it with pre-populated headers
try:
    password_file = pandas.read_csv(PASSWORD_PATH)
except FileNotFoundError:
    df = pandas.DataFrame(columns=["Website", "Email", "Password"])
    df.to_csv(PASSWORD_PATH, index=False)

# ---------------------------- BUTTON HANDLERS ------------------------------- #
def list_password():
    # checking if the file is empty
    password_file = pandas.read_csv(PASSWORD_PATH)
    if password_file.empty:
        messagebox.showinfo("Error", "There are no passwords stored.")
        return
    password_window = tkinter.Toplevel(bg=GREY)
    password_window.title('Password Viewer')
    password_window.geometry('600x350')
    table = pandastable.Table(password_window, dataframe=password_file) # creating table inside toplevel window
    options = {'fontsize': 10, 'cellbackgr': GREY, 'textcolor': WHITE, 'rowselectedcolor': '#875484'}
    pandastable.config.apply_options(options, table)
    table.show()


def write_to_file():
    # need to re-read the passwords every time to compare them
    passwords = pandas.read_csv(PASSWORD_PATH)['Password'].to_list()
    email = email_entry.get()
    web = web_entry.get()
    passw = pass_entry.get()
    response = True         # Check for the same password. True by default
    if not email or not web or not passw:
        messagebox.showwarning(title="Empty form", message='Please fill in all fields!')
    else:
        # check if the password is already in use. Notify user in this case
        if passw in passwords:
            response = messagebox.askyesno(title="Same password found", message=f"The password '{passw}' is already used by another website. Do you wish to continue?")
        if response:
            web_entry.delete(0, tkinter.END)
            pass_entry.delete(0, tkinter.END)
            to_file = pandas.DataFrame({"Website": web, "Email": email, "Password": str(passw)}, index=[0])
            to_file.to_csv(PASSWORD_PATH, mode='a', index=False, header=not os.path.exists(PASSWORD_PATH))


def generate_password():
    # clear the entry object before generating a password
    if pass_entry.get():
        pass_entry.delete(0, tkinter.END)
    password_letters = [random.choice(letters) for letter in range(random.randint(8, 10))]
    password_numbers = [random.choice(numbers) for number in range(random.randint(2, 4))]
    password_symbols = [random.choice(symbols) for symbol in range(random.randint(2, 4))]
    password_list = password_symbols + password_letters + password_numbers
    random.shuffle(password_list)
    paswd = "".join(password_list)
    pass_entry.insert(0, paswd)
    pyperclip.copy(paswd) # copy to clipboard

# ---------------------------- MAIN UI SETUP ------------------------------- #
window = tkinter.Tk()
window.config(padx=20, pady=20, bg=GREY)
window.title("Password Manager")

logo = tkinter.PhotoImage(file='logo.png')
canvas = tkinter.Canvas(width=200, height=200, bg=GREY, highlightthickness=0)
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# Labels
website = tkinter.Label(text="Website: ", bg=GREY, fg=WHITE, highlightthickness=0, padx=5, pady=5)
website.grid(row=1, column=0)
email = tkinter.Label(text="Email/Username: ", bg=GREY, fg=WHITE, highlightthickness=0, padx=5, pady=5)
email.grid(row=2, column=0)
password = tkinter.Label(text="Password: ", bg=GREY, fg=WHITE, highlightthickness=0, padx=5, pady=5)
password.grid(row=3, column=0)

# Entries
web_entry = tkinter.Entry(width=35, bg=GREY, fg=WHITE, highlightthickness=0)
web_entry.grid(row=1, column=1, columnspan=2)
web_entry.focus()
email_entry = tkinter.Entry(width=35, bg=GREY, fg=WHITE, highlightthickness=0)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, 'test@test.com')
pass_entry = tkinter.Entry(width=21, bg=GREY, fg=WHITE, highlightthickness=0)
pass_entry.grid(row=3, column=1)

# Buttons
pass_button = tkinter.Button(text="Generate Password", command=generate_password, highlightbackground=GREY, highlightthickness=0)
pass_button.grid(row=3, column=2)
add_button = tkinter.Button(text="Add", width=36, command=write_to_file, highlightbackground=GREY, highlightthickness=0,)
add_button.grid(row=4, column=1, columnspan=2, padx=5, pady=2)
view_pass = tkinter.Button(text="View Passwords", width=36, command=list_password, highlightbackground=GREY, highlightthickness=0)
view_pass.grid(row=5, column=1, columnspan=2, padx=5, pady=10)

window.mainloop()
