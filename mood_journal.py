# Import necessary modules
import tkinter as tk                            # For the graphical user interface
from tkinter import messagebox                  # For popup alert dialogs
from nltk.sentiment import SentimentIntensityAnalyzer  # Sentiment analysis tool
import nltk                                     # Natural Language Toolkit (NLP tools)
import requests                                 # For fetching quotes from the internet
import matplotlib.pyplot as plt                 # For plotting mood trends over time
import csv                                      # To save mood data to a CSV file
import os                                       # To check if a file exists
from datetime import datetime                   # To track the current date

# Download the VADER sentiment model if it's not already present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

# Create the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to detect the mood of a journal entry
def detect_mood(text):
    score = sia.polarity_scores(text)["compound"]  # Get the compound sentiment score
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Function to fetch an inspirational quote from the web
def fetch_quote():
    try:
        res = requests.get("https://api.quotable.io/random", timeout=5)
        if res.status_code == 200:
            return res.json().get("content", "Stay positive and keep going!")
        return "Stay positive and keep going!"
    except Exception:
        return "Stay positive and keep going!"

# Function to save the detected mood to a CSV file
def save_mood(mood):
    filename = "mood_log.csv"
    file_exists = os.path.exists(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Mood"])  # Write header if file is new
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), mood])

# Function to plot mood trend from the CSV file
def plot_mood_trend():
    filename = "mood_log.csv"
    
    if not os.path.exists(filename):
        messagebox.showinfo("No Data", "No mood data found.")
        return

    # Load mood data from the file
    dates, moods = [], []
    mood_map = {"Positive": 1, "Neutral": 0, "Negative": -1}

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(row["Date"])
            moods.append(mood_map.get(row["Mood"], 0))

    # Plot the mood trend
    plt.figure(figsize=(10, 5))
    plt.plot(dates, moods, marker='o', linestyle='-', color='blue')
    plt.title("Mood Over Time")
    plt.xlabel("Date")
    plt.ylabel("Mood (1=Positive, 0=Neutral, -1=Negative)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Function to handle journal submission
def submit_entry(text_widget, result_label, quote_label):
    text = text_widget.get("1.0", tk.END).strip()  # Get the user's text from the textbox
    
    if not text:
        messagebox.showwarning("Empty Entry", "Please write something.")
        return
    
    mood = detect_mood(text)       # Analyze mood
    save_mood(mood)                # Save mood to CSV
    quote = fetch_quote()          # Get an inspirational quote
    
    # Show results in the GUI
    result_label.config(text=f"Mood: {mood}")
    quote_label.config(text=f"Inspiration: {quote}")

# Main function to run the GUI
def main():
    # Create the main window
    window = tk.Tk()
    window.title("Mood Journal")

    # Label for instruction
    tk.Label(window, text="Write your journal entry:").pack()

    # Text area for journal input
    text_widget = tk.Text(window, height=10, width=50)
    text_widget.pack(pady=5)

    # Label to show mood result
    result_label = tk.Label(window, text="")
    result_label.pack()

    # Label to show inspirational quote
    quote_label = tk.Label(window, text="", wraplength=400, fg="gray")
    quote_label.pack(pady=5)

    # Button to submit journal entry
    tk.Button(
        window, 
        text="Submit Entry", 
        command=lambda: submit_entry(text_widget, result_label, quote_label)
    ).pack(pady=5)

    # Button to show mood trend chart
    tk.Button(
        window, 
        text="Show Mood Trend", 
        command=plot_mood_trend
    ).pack()

    # Start the GUI event loop
    window.mainloop()

# Entry point of the program
if __name__ == "__main__":
    main()