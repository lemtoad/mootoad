import openai
from collections import deque
from textblob import TextBlob
import pickle

# Set up the OpenAI API key
openai.api_key = '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'  # Replace 'your-api-key' with your actual API key

class Lembot:
    def __init__(self):
        # Lembot initialization code, if any.
        self.user_profiles = {}

    def greet_user(self, user_id):
        if user_id not in self.user_profiles:
            self.create_user_profile(user_id)
            return "Hello! I am Lembot, your ultimate AI assistant. How can I assist you today?"
        else:
            return f"Welcome back! How can I assist you today?"

    def get_information(self):
        return "I am Lembot, your ultimate AI assistant. I'm here to help and provide information."

    def perform_action(self, action):
        # Implement code to perform specific actions based on user requests.
        pass

    def create_user_profile(self, user_id):
        # Create a new user profile
        self.user_profiles[user_id] = {}

    def save_user_profiles(self):
        # Save user profiles to a file using pickle
        with open("user_profiles.pkl", "wb") as file:
            pickle.dump(self.user_profiles, file)

    def load_user_profiles(self):
        try:
            # Load user profiles from the saved file using pickle
            with open("user_profiles.pkl", "rb") as file:
                self.user_profiles = pickle.load(file)
        except FileNotFoundError:
            pass

class Conversation:
    def __init__(self, max_tokens=4096, max_tokens_per_message=1024):
        self.max_tokens = max_tokens
        self.max_tokens_per_message = max_tokens_per_message
        self.tokens = deque()
        self.context = ""

    def add_message(self, role, content):
        # Ensure the message fits within the token limit
        if len(content) > self.max_tokens_per_message:
            content = content[:self.max_tokens_per_message]

        if role == "user":
            # To preserve context, append the user message to the existing context
            self.context += content

        # Use a sliding window to maintain context while handling token limits
        context_tokens = self.context.split()[-(self.max_tokens - len(content)):]
        context = " ".join(context_tokens)

        message = {"role": role, "content": content, "context": context}

        # Update context and token history
        self.context = context
        self.tokens.append(message)

    def get_messages(self):
        return [message for message in self.tokens]

def get_emotion(sentiment_value):
    if sentiment_value >= 0.1:
        return "positive"
    elif sentiment_value <= -0.1:
        return "negative"
    else:
        return "neutral"

def get_ai_response(user_id, user_message, temperature=0.7, max_tokens=1024):
    conversation.add_message("user", user_message)

    # Prepare the messages for API call (without the 'context' property)
    messages_for_api = [{"role": message["role"], "content": message["content"]} for message in conversation.get_messages()]

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can choose a different model if you prefer
        messages=messages_for_api,
        temperature=temperature,
        max_tokens=max_tokens
    )

    # Extract the assistant's message from the response
    assistant_message = response.choices[0].message['content']

    # Perform sentiment analysis on the user's message
    blob = TextBlob(user_message)
    sentiment_value = blob.sentiment.polarity
    emotion = get_emotion(sentiment_value)

    # Modify Lembot's response based on user's emotion
    if emotion == "positive":
        assistant_message = f"That's great to hear! {assistant_message}"
    elif emotion == "negative":
        assistant_message = f"I'm sorry to hear that. {assistant_message}"
    else:
        assistant_message = f"{assistant_message}"

    # Add the assistant's message to the conversation history
    conversation.add_message("assistant", assistant_message)

    return assistant_message

# Create a global conversation instance
conversation = Conversation()
