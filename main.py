import os
from tkinter import *
from PIL import ImageTk, Image
import requests
import math
import sys



class SpeedTypingApp:
    def __init__(self):
        # Initialize global variables
        self.play_again_button = None
        self.timer = False
        self.entries = []
        self.correct_entries = []
        self.incorrect_entries = []
        self.quotes = []
        self.final_time = 0
        self.wpm = 0
        self.high_score = 0

        # Set up constants
        self.api_key = 'YOUR_API_KEY'
        self.web_page = 'https://api.api-ninjas.com/v1/quotes'
        self.timer_time = 60

        # Set up the main window
        self.window = Tk()
        self.window.config(bg="yellow")
        self.setup_welcome_screen()
        self.window.mainloop()

    def fetch_quote(self):
        """Fetch a random quote from the API."""
        headers = {'X-Api-Key': self.api_key}
        response = requests.get(self.web_page, headers=headers)
        return response.json()[0]['quote']

    def setup_welcome_screen(self):
        """Display the welcome screen."""
        self.canvas = Canvas(height=300, width=400, bg="yellow", bd=0, highlightbackground="yellow")
        try:
            self.img = Image.open("meter-speedometer-transparent-free-png.png")
            self.img = ImageTk.PhotoImage(self.img)
            self.canvas.create_image(200, 200, image=self.img)
        except FileNotFoundError:
            print("File not found. Download your own image and run again.")
        self.canvas.grid(column=0, row=0, pady=(20, 0))
        self.canvas.create_text(200, 70, text="Welcome to the speed typing app", font=('Courier', 16, 'bold'),
                                fill="black")

        self.start_typing_button = Button(self.window, text="Start Typing", bd=0, bg="yellow",
                                          highlightbackground="yellow",
                                          font=('Arial', 26), padx=10, pady=10, command=self.setup_typing_screen)
        self.start_typing_button.grid(column=0, row=1, pady=(20, 80))

    def setup_typing_screen(self):
        """Set up the typing test screen."""
        self.canvas.destroy()
        self.start_typing_button.destroy()



        self.window.geometry("800x750")

        self.top_canvas = Canvas(height=80, width=800, bg="yellow", bd=0, highlightbackground="yellow")
        self.top_canvas.grid(column=0, row=0)

        self.text_canvas = Canvas(height=500, width=720, bg="white")
        self.text_canvas.grid(column=0, row=1)

        self.welcome_text_id = self.text_canvas.create_text(10, 10, text="How fast are your fingers?\n"
                                                                         "Do the one-minute typing test to find out!\n"
                                                                         "Press the space bar after each word.\n"
                                                                         "At the end, you'll get your typing speed in CPM and WPM.\n"
                                                                         "The timer will begin as soon as you start typing.\n"
                                                                         "Click the Start button when you are ready.\nGood luck!",
                                                            fill="black", font=("Courier", 24), anchor=NW)

        self.start_button = Button(self.window, text="Start", bd=0, bg="yellow", highlightbackground="yellow",
                                   font=('Arial', 26), padx=10, pady=10, command=self.start_typing_test)
        self.start_button.grid(column=0, row=2, pady=40)

    def start_typing_test(self):
        """Start the typing test."""
        self.entries = []
        self.correct_entries = []
        self.incorrect_entries = []
        self.quotes = []

        self.top_canvas.delete("all")
        self.text_canvas.delete("all")

        try:
            self.play_again_button.destroy()
            self.exit_button.destroy()
            print("Yo")
        except NameError:
            print("Hi")
            pass
        except AttributeError:
            print("Hello")
            pass

        self.start_button.destroy()

        self.score_text = self.top_canvas.create_text(50, 40, text=f"High score: {self.high_score} WPM ", anchor=W,
                                                      fill="black", font=("Courier", 24))
        self.timer_text = self.top_canvas.create_text(600, 40, text="Timer: 1:00", anchor=W, fill="black",
                                                      font=("Courier", 24))

        quote = self.fetch_quote()
        self.quotes = quote.split()

        print(len(self.quotes))

        characters = 0
        for i in range(len(self.quotes)):
            if characters + 1 + len(self.quotes[i]) < 48:
                characters += len(self.quotes[i]) + 1
            else:
                self.quotes[i] = ('\n' + self.quotes[i])
                characters = len(self.quotes[i]) - 1

        final_quote = ' '.join(self.quotes)
        self.text_canvas.delete(self.welcome_text_id)

        self.word_entry = Entry(self.window, font=('Arial', 24))
        self.word_entry.grid(column=0, row=2, pady=(20, 80))
        self.word_entry.bind('<space>', self.handle_space_bar)
        self.word_entry.bind('<Key>', self.start_timer)

        self.quote_text = self.text_canvas.create_text(10, 10, text=final_quote, anchor=NW, fill="black",
                                                       font=("Courier", 24))

    def handle_space_bar(self, event):
        """Handle space bar presses."""
        entry_text = self.word_entry.get()
        self.word_entry.delete(0, END)

        if entry_text and entry_text != ' ':
            self.entries.append(entry_text)

        if len(self.entries) == len(self.quotes):
            for i in range(len(self.entries)):
                if self.entries[i].replace(' ', '') == self.quotes[i].replace('\n', ''):
                    self.correct_entries.append(self.entries[i].replace(' ', ''))
                else:
                    self.incorrect_entries.append(self.entries[i].replace(' ', ''))
            self.end_typing_test()

    def start_timer(self, event):
        """Start the timer if it is not already running."""
        if not self.timer:
            self.count_down(self.timer_time)
            self.timer = True

    def count_down(self, count):
        """Update the countdown timer."""
        count_min = math.floor(count / 60)
        count_sec = count % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        self.top_canvas.itemconfig(self.timer_text, text=f"Timer: {count_min}:{count_sec}")
        if count > 0:
            self.timer = self.window.after(1000, self.count_down, count - 1)
            self.final_time = count
        else:
            self.final_time = 0
            self.end_typing_test()

    def end_typing_test(self):
        """Handle the end of the typing test."""

        if len(self.entries) != len(self.quotes):
            for i in range(len(self.entries)):
                if self.entries[i].replace(' ', '') == self.quotes[i].replace('\n', ''):
                    self.correct_entries.append(self.entries[i].replace(' ', ''))
                else:
                    self.incorrect_entries.append(self.entries[i].replace(' ', ''))

        self.word_entry.destroy()
        self.window.after_cancel(self.timer)
        self.text_canvas.delete(self.quote_text)

        self.timer = False
        self.wpm = round(((len(self.correct_entries)) / (60 - self.final_time)) * 60, 2)

        if hasattr(self, 'results_text'):
            self.text_canvas.delete(self.results_text)

        self.results_text = self.text_canvas.create_text(360, 250,
                                                         text=f"You spelled {len(self.correct_entries)} words correctly.\n"
                                                              f"You misspelled {abs(len(self.correct_entries) - len(self.quotes))} words.\n"
                                                              f"(Remember caps and punctuation)\n\nYour typing speed is: {self.wpm} WPM",
                                                         anchor=CENTER, fill="black", font=("Courier", 24))

        self.play_again_button = Button(self.window, text="Play Again", anchor=CENTER, padx=10, pady=10,
                                        command=self.start_typing_test, font=('Courier', 24))
        self.play_again_button.place(x=300, y=500)

        self.exit_button = Button(self.window, text="Exit", anchor=CENTER, padx=5, pady=5, command=sys.exit,
                                  font=('Courier', 12), bd=0)
        self.exit_button.place(x=360, y=100)

        self.check_high_score()

    def check_high_score(self):
        """Update and display the high score."""
        if self.wpm > self.high_score:
            self.high_score = self.wpm
            self.top_canvas.itemconfig(self.score_text, text=f"High score: {self.high_score} WPM")


if __name__ == "__main__":
    SpeedTypingApp()



