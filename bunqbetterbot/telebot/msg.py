BOT_NAME = 'bunqBetterBot'
SESSION_DURATION = 5

WELCOME = "Hello there! You can use my funky functionality to be even more happy with bunq!"
UPDATE = "You spent {} Euro of your {} budget {}"

CANCEL = "You canceled the process. Will delete all information."
INVALID_INPUT = "Some of the information you gave were incorrect. Try again :-("
INVALID_INPUT_NUMBER = "Invalid input. Please enter a number."
NO_PERMISSION = "You don't have permission to contact this bot!"
ERROR = "Sorry, but an error occurred on my side."

HOME = "Welcome to the Home menu. Where do you want to go?"
ACCOUNT = "Here are some Account functions:"
FUNCTIONS = "Here is what I can do for you:"

DELETE_MSG = "For security, please delete the previous message containing the {}.\n" \
             "On iOS: Press long on message > More > Trash > Delete for me and {msg.BOT_NAME}\n" \
             "On macOS: Right click message > Check 'Delete for {msg.BOT_NAME} > Delete\n" \
             "On Android: I have no clue."

REGISTER_START = "You want to register! Great!\n"
REGISTER_ENV = "Tell me whether this is a Sandbox or Production account:"
REGISTER_KEY = "Now, please send me your API key:"
REGISTER_PASS = "And finally, to protect your account, send me a secure password:"
REGISTER_END = "Account created! Congratulations!\n" \
               "Press Login to create a session."

LOGIN_START = "Please send me your password:"
LOGIN_FAIL = "Sorry, but your password does not match our records.\n" \
             "Please edit your message and insert another password."
LOGIN_END = f"You're logged in!\n\n" \
            f"Your session will last {SESSION_DURATION}min before you have to log in again."

CREATE_START = "You want to create a new Budget! Great! Let's get going right away"
CREATE_NAME = "Please enter a name for the new Budget"
CREATE_IBAN = "Next, select the accounts, which the Budget should monitor and click 'Done' when " \
              "you're finished."
CREATE_DURATION = "How many days should the new Budget cover?"
CREATE_DURATION_MORE = "Enter a number for how many days the Budget should cover"
CREATE_FINISH = "Congratulations! You created a new Budget!"
