import tkinter as tk
import account_functions as acc
import image_functions 
import voice_functions 
import cv2

# Environment Variables
BACKGROUND = "#192329"
BUTTON_FONT = ("Calibri", 12, "normal")
BUTTON_COLOR = "#1A79AF"
FONT = ("Calibri", 24, "normal")
FONT_SMALL = ("Calibri", 15, "normal")
ENTRY_FONT = ("Calibri", 12, "normal")
TEXT_COLOR = "#FFFFFF"

window = tk.Tk()
user = acc.Account()

# Setting up the user interface and loading data
window.title("Secure-A")
window.minsize(height=300, width=500)
window.config(bg=BACKGROUND)
title_image = tk.PhotoImage(file="auto_logout_system/title.png")

def clear_window():
    """Clears all the widgets currently present on the window"""
    for widget in window.place_slaves():
        widget.destroy()

def title_screen():
    """Loads the title screen"""
    title_image_label = tk.Label(image=title_image)
    title_image_label.place(x=-2, y=-2)
    get_started_button = tk.Button(text="Get Started", command=detecting_face_screen)
    get_started_button.config(font=BUTTON_FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR, width=12)
    get_started_button.place(relx=0.1, rely=0.6)

def detecting_face_screen():
    """Captures user's live image and compares with saved images"""
    clear_window()
    image_functions.load_data()
    user.image = None
    detecting_face_label = tk.Label(text="Detecting Face")
    detecting_face_label.config(font=FONT, bg=BACKGROUND, fg=TEXT_COLOR)
    detecting_face_label.place(relx=0.5, rely=0.3, anchor="center")
    window.update()
    
    while user.image is None:
        user.image = image_functions.capture_image()
    user.face_encodings = image_functions.find_encodings(user.image)
    user.uniqueId = image_functions.compare_face(user.face_encodings)
    window.after(1000, cv2.destroyAllWindows)

    if user.uniqueId == "Unknown":
        detecting_face_label.config(text="Unknown user")
        sign_up_button = tk.Button(text="Sign-up", command=sign_up_screen)
        sign_up_button.config(font=BUTTON_FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR, width=12)
        sign_up_button.place(relx=0.4, rely=0.5)

    else:
        user.getdata()
        detecting_face_label.config(text=f"Are you {user.name}?")
        passkey = tk.StringVar()
        passkey_label = tk.Label(text= "Password: ")
        passkey_label.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR)
        passkey_label.place(relx=0.15, rely=0.5, anchor="w")
        passkey_entry = tk.Entry(textvariable=passkey, show='•')
        passkey_entry.config(width=30, font=ENTRY_FONT)
        passkey_entry.place(relx=0.35, rely=0.465)
        sign_in_button = tk.Button(text="Sign-in", command=sign_in_screen)
        sign_in_button.config(font=BUTTON_FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR, width=12)
        sign_in_button.place(relx=0.25, rely=0.7)
        sign_up_button = tk.Button(text="Sign-up", command=sign_up_screen)
        sign_up_button.config(font=BUTTON_FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR, width=12)
        sign_up_button.place(relx=0.55, rely=0.7)

def sign_up_screen():
    clear_window()
    user.name = tk.StringVar()
    user.password = tk.StringVar()
    user.secure_linkedin = tk.IntVar()
    user.secure_instagram = tk.IntVar()

    name_label = tk.Label(text= "Name: ")
    name_label.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR)
    name_label.place(relx=0.15, rely=0.2, anchor="w")
    name_entry = tk.Entry(textvariable=user.name)
    name_entry.config(width=32, font=ENTRY_FONT)
    name_entry.place(relx=0.35, rely=0.165)
    password_label = tk.Label(text= "Password: ")
    password_label.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR)
    password_label.place(relx=0.15, rely=0.35, anchor="w")
    password_entry = tk.Entry(textvariable=user.password, show='•')
    password_entry.config(width=32, font=ENTRY_FONT)
    password_entry.place(relx=0.35, rely=0.315)
    secure_label = tk.Label(text= "What would you like to secure? ")
    secure_label.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR)
    secure_label.place(relx=0.25, rely=0.5, anchor="w")
    linkedin_check = tk.Checkbutton(text="LinkedIn", variable=user.secure_linkedin)
    linkedin_check.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR, selectcolor=BACKGROUND)
    linkedin_check.place(relx=0.25, rely=0.6)
    instagram_check = tk.Checkbutton(text="Instagram", variable=user.secure_instagram)
    instagram_check.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR, selectcolor=BACKGROUND)
    instagram_check.place(relx=0.55, rely=0.6)
    submit_button = tk.Button(text="Submit", command=read_account_details)
    submit_button.config(font=BUTTON_FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR, width=12)
    submit_button.place(relx=0.35, rely=0.8)
    
def read_account_details():
    clear_window()
    user.linkedin_username = tk.StringVar()
    user.linkedin_password = tk.StringVar()
    user.instagram_username = tk.StringVar()
    user.instagram_password = tk.StringVar()   

    if user.secure_linkedin.get() == 1:
        linkedin_username_label = tk.Label(text="LinkedIn username: ")
        linkedin_username_label.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR)
        linkedin_username_label.place(relx=0.05, rely=0.2, anchor="w")
        linkedin_username_entry = tk.Entry(textvariable=user.linkedin_username)
        linkedin_username_entry.config(width=30, font=ENTRY_FONT)
        linkedin_username_entry.place(relx=0.45, rely=0.165)
        linkedin_password_label = tk.Label(text="LinkedIn Password: ")
        linkedin_password_label.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR)
        linkedin_password_label.place(relx=0.05, rely=0.35, anchor="w")
        linkedin_password_entry = tk.Entry(textvariable=user.linkedin_password, show='•')
        linkedin_password_entry.config(width=30, font=ENTRY_FONT)
        linkedin_password_entry.place(relx=0.45, rely=0.315)

    if user.secure_instagram.get() == 1:  
        instagram_username_label = tk.Label(text="Instagram username: ")
        instagram_username_label.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR)
        instagram_username_label.place(relx=0.05, rely=0.5, anchor="w")
        instagram_username_entry = tk.Entry(textvariable=user.instagram_username)
        instagram_username_entry.config(width=30, font=ENTRY_FONT)
        instagram_username_entry.place(relx=0.45, rely=0.47)
        instagram_password_label = tk.Label(text="Instagram Password: ")
        instagram_password_label.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR)
        instagram_password_label.place(relx=0.05, rely=0.65, anchor="w")
        instagram_password_entry = tk.Entry(textvariable=user.instagram_password, show='•')
        instagram_password_entry.config(width=30, font=ENTRY_FONT)
        instagram_password_entry.place(relx=0.45, rely=0.62)
    
    submit_button = tk.Button(text="Submit", command=create_account)
    submit_button.config(font=BUTTON_FONT, bg=BUTTON_COLOR, fg=TEXT_COLOR, width=12)
    submit_button.place(relx=0.35, rely=0.8)

def create_account():
    clear_window()
    user.sign_up()
    account_created_label = tk.Label(text="Account Created Successfully!")
    account_created_label.config(font=FONT, bg=BACKGROUND, fg=TEXT_COLOR)
    account_created_label.place(relx=0.5, rely=0.3, anchor="center")
    window.after(2000, title_screen)

def sign_in_screen():
    clear_window()
    image_functions.update_image(user)
    welcome_label = tk.Label(text=f"Welcome, {user.name}")
    welcome_label.config(font=FONT, bg=BACKGROUND, fg=TEXT_COLOR)
    welcome_label.place(relx=0.5, rely=0.2, anchor="center")
    options_label = tk.Label(text="What would you like to use?")
    options_label.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR)
    options_label.place(relx=0.5, rely=0.35, anchor="center")
    options_frame = tk.Frame(bg=BACKGROUND)
    options_frame.place(relx=0.5, rely=0.6, anchor="center")
    radio_state = tk.IntVar()

    if user.secure_linkedIn==True:
        login_linkedin = tk.Radiobutton(options_frame, text="LinkedIn", value=1, variable=radio_state, command=lambda:log_in(radio_state))
        login_linkedin.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR, selectcolor=BACKGROUND)
        login_linkedin.grid(row=0, column=0)
    if user.secure_instagram==True:
        login_instagram = tk.Radiobutton(options_frame, text="Instagram", value=2, variable=radio_state, command=lambda:log_in(radio_state))
        login_instagram.config(font=FONT_SMALL, bg=BACKGROUND, fg=TEXT_COLOR, selectcolor=BACKGROUND)
        login_instagram.grid(row=1, column=0)

    window.update()
    voice_functions.operations(user, window)

def log_in(radio_state):
    if radio_state.get() == 1:
        user.login_linkedin(window)
    elif radio_state.get() == 2:
        user.login_instagram(window)

title_screen()
window.mainloop()