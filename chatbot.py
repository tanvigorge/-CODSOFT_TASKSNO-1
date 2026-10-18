"""A small rule-based chatbot that runs in the terminal."""

from datetime import datetime
import re


EXIT_COMMANDS = {"bye", "goodbye", "quit", "exit", "see you"}


def normalize_input(user_input: str) -> str:
    message = re.sub(r"[^a-z0-9'\s]", " ", user_input.lower())
    return " ".join(message.split())


def extract_user_name(user_input: str) -> str | None:
    match = re.search(r"\b(?:i am|i'm|my name is)\s+([a-z]+)\b", user_input.lower())
    if match:
        return match.group(1).capitalize()
    return None


def get_response(user_input: str, user_name: str | None = None) -> str:
    """Return a response selected from a few simple text-matching rules."""
    message = normalize_input(user_input)
    introduced_name = extract_user_name(user_input)

    if message in EXIT_COMMANDS:
        return "Goodbye! It was nice chatting with you."
    elif re.search(r"\b(hello|hi|hey)\b", message):
        return "Hello! How can I help you today?"
    elif introduced_name:
        return f"Nice to meet you, {introduced_name}!"
    elif re.search(r"\b(?:your|ur)\s+name\b|\bwho are you\b", message):
        return "I'm RuleBot, a simple chatbot powered by predefined rules."
    elif re.search(r"\b(?:what'?s|what|whats|wht'?s|wht|whts)\s+(?:is\s+)?my\s+name\b", message):
        if user_name:
            return f"Your name is {user_name}."
        return "You haven't told me your name yet."
    elif re.search(r"\b(?:what'?s|what|whats|wht'?s|wht|whts)\s+(?:is\s+)?(?:your|ur)\s+name\b", message):
        return "I'm RuleBot, a simple chatbot powered by predefined rules."
    elif re.search(r"\b(how are you|how's it going)\b", message):
        return "I'm doing well, thanks for asking! How are you?"
    elif re.search(r"\b(time|what time is it)\b", message):
        return f"The current time is {datetime.now().strftime('%I:%M %p')}"
    elif re.search(r"\b(date|what day is it)\b", message):
        return f"Today's date is {datetime.now().strftime('%A, %B %d, %Y')}"
    elif re.search(r"\b(thanks|thank you)\b", message):
        return "You're welcome!"
    elif re.search(r"\b(help|what can you do)\b", message):
        return "Try saying hello, asking my name, asking for the time or date, or saying bye."
    else:
        return "I'm not sure how to respond to that yet. Try asking for help."


def main() -> None:
    print("RuleBot: Hello! Type 'help' to see what I can do, or 'bye' to exit.")
    user_name = None

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nRuleBot: Goodbye!")
            break

        response = get_response(user_input, user_name)
        print(f"RuleBot: {response}")

        user_name = extract_user_name(user_input) or user_name
        if normalize_input(user_input) in EXIT_COMMANDS:
            break


if __name__ == "__main__":
    main()