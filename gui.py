import tkinter as tk
from tkinter import scrolledtext, ttk
from ai_model import get_ai_response, Lembot  # Import the Lembot class
from textblob import TextBlob

class LembotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Lembot - The Ultimate AI Assistant")
        master.geometry("1200x800")  # Enlarged window size
        master.resizable(False, False)

        # Set colors for user and AI chats
        self.user_color = "#007bff"  # Blue
        self.ai_color = "#ff6b6b"    # Red

        # Create a chat history frame
        self.chat_history_frame = tk.Frame(master, bg="white")
        self.chat_history_frame.pack(fill=tk.BOTH, expand=True)

        # Create a chat history with scrollbar
        self.chat_history = scrolledtext.ScrolledText(self.chat_history_frame, wrap=tk.WORD, width=100, height=20, font=("Arial", 12))
        self.chat_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.chat_history.config(state=tk.DISABLED)

        # Create a user input frame
        self.user_input_frame = tk.Frame(master, bg="white")
        self.user_input_frame.pack(fill=tk.BOTH)

        # Create user name entry
        self.user_name_label = tk.Label(self.user_input_frame, text="Your Name:", font=("Arial", 12))
        self.user_name_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.user_name_entry = tk.Entry(self.user_input_frame, width=30, font=("Arial", 12))  # Enlarged input box
        self.user_name_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Create user emotion display
        self.user_emotion_label = tk.Label(self.user_input_frame, text="Your Emotion: Neutral", font=("Arial", 12))
        self.user_emotion_label.pack(side=tk.LEFT, padx=5, pady=5)

        # Create Lembot AI model instance
        self.lem_bot = Lembot()

        # Create a "Send" button
        self.send_button = tk.Button(self.user_input_frame, text="Send", command=self.send_message, font=("Arial", 12))
        self.send_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a status bar to display additional information
        self.status_bar = tk.Label(master, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 12))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create user input field
        self.user_input = scrolledtext.ScrolledText(self.user_input_frame, wrap=tk.WORD, width=80, height=4, font=("Arial", 12))
        self.user_input.pack(side=tk.LEFT, padx=5, pady=5)

    def send_message(self):
        user_message = self.user_name_entry.get() + ": " + self.user_input.get("1.0", tk.END).strip()
        if user_message and user_message != ": ":
            user_name = self.user_name_entry.get()
            if not user_name:
                user_name = "You"

            # Perform sentiment analysis on the user's message
            blob = TextBlob(user_message)
            sentiment_value = blob.sentiment.polarity
            emotion = self.get_emotion(sentiment_value)
            self.user_emotion_label.config(text=f"Your Emotion: {emotion.capitalize()}")

            # Display user message in chat history
            self.display_message(user_name, user_message, self.user_color)

            # Get Lembot's response by calling the get_ai_response function from ai_model.py
            ai_response = get_ai_response(user_name, user_message)
    
            # Display Lembot's response in chat history
            self.display_message("Lembot", ai_response, self.ai_color)

            # Update status bar with additional information
            self.status_bar.config(text=f"{user_name} sent a message. Lembot replied.")

            # Save user profiles after the conversation
            lem_bot.save_user_profiles()
            
    def display_message(self, sender, message, color):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"{sender}: {message}\n", color)
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)
        self.user_input.delete("1.0", tk.END)

    def get_emotion(self, sentiment_value):
        if sentiment_value >= 0.1:
            return "positive"
        elif sentiment_value <= -0.1:
            return "negative"
        else:
            return "neutral"


if __name__ == "__main__":
    root = tk.Tk()
    app = LembotGUI(root)
    root.mainloop()
