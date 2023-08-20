from tkinter import *
import pyshorteners

root = Tk()
root.title("URL Shortener")
root.geometry('550x300')
root.resizable(False, False)
root.configure(bg="white")

def shorten_url():
    url = long_url.get()
    type_tiny = pyshorteners.Shortener()
    shortened_url = type_tiny.tinyurl.short(url)
    display_url(shortened_url)

def display_url(shortened_url):
    short_url.delete(0, END)
    short_url.insert(0, shortened_url)

def reset():
    long_url.delete(0, END)
    short_url.delete(0, END)

def copy_to_clipboard():
    shortened_url = short_url.get()
    root.clipboard_clear()
    root.clipboard_append(shortened_url)

# Set a soft pastel color palette
pastel_blue = "#AEC6CF"
pastel_green = "#B2D8B2"
pastel_pink = "#F4B3C2"

root.configure(bg=pastel_blue)  # Set the background color

# Header Label
header_label = Label(root, 
                     text="URL Shortener", 
                     font=("Times New Roman", 24, "bold"), 
                     bg=pastel_blue, 
                     fg="black")
header_label.grid(row=0, column=1, padx=10, pady=10, columnspan=1)

# Labels
enter_url = Label(root, 
                  text="Enter URL:", 
                  font=("Arial", 18), 
                  bg=pastel_blue)
enter_url.grid(row=1, column=0, padx=10, pady=10)

output = Label(root, 
               text="Output:", 
               font=("Arial", 18), 
               bg=pastel_blue)
output.grid(row=2, column=0, padx=10, pady=10)

# Entry Fields
long_url = Entry(root, font=("Arial", 14))
long_url.grid(row=1, column=1, padx=10, pady=10)

short_url = Entry(root, font=("Arial", 14))
short_url.grid(row=2, column=1, padx=10, pady=10)

# Buttons
output_button = Button(root, 
                       text="Shorten URL", 
                       font=("Arial", 14), 
                       command=shorten_url, 
                       bg=pastel_green)
output_button.grid(row=1, column=2, padx=10, pady=10)

reset_button = Button(root, 
                      text="Reset", 
                      font=("Arial", 14), 
                      command=reset, 
                      bg='#FFFFB3')
reset_button.grid(row=2, column=2, padx=10, pady=10)

copy_button = Button(root, 
                     text="Copy to Clipboard", 
                     font=("Arial", 14), 
                     command=copy_to_clipboard,
                     bg="royal blue", 
                     fg="white")
copy_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

exit_button = Button(root, 
                     text="Exit", 
                     font=("Arial", 14), 
                     command=root.quit, 
                     bg=pastel_pink)
exit_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
