import app.validators.shared_validator as shared_validator
from app.config import config
from app import exceptions
import re, logging

EMAIL_PATTERN = re.compile(r"^[a-zA-ZąčęėįšųūžĄČĘĖĮŠŲŪŽ0-9._%+-]+@[a-zA-ZąčęėįšųūžĄČĘĖĮŠŲŪŽ0-9-]+\.[a-zA-Z]{2,}$")
NAME_PATTERN = re.compile(r"[^a-zA-ZąčęėįšųūžĄČĘĖĮŠŲŪŽ]")
NUMBER_PATTERN = re.compile(r"[0-9]")

#Validate username to make sure it has no special symbols, SQL queries and length of username is within specified bounds
def validate_username(username: str):
    if not username:
        logging.warning("No username provided")
        raise exceptions.UnprocessableEntity("Vartotojo vardas yra privalomas!")

    shared_validator.validate_sql_malicious_input(username)

    username_length = len(username)
    if username_length < config.MIN_USERNAME_LENGTH:
        logging.warning("Provided username is too short")
        raise exceptions.UnprocessableEntity(f"Vartotojo vardas privalo turėti ne mažiau kaip {config.MIN_USERNAME_LENGTH} simbolius!")
    
    if username_length > config.MAX_USERNAME_LENGTH:
        logging.warning("Provided username is too long")
        raise exceptions.UnprocessableEntity(f"Vartotojo vardas privalo turėti ne daugiau kaip {config.MAX_USERNAME_LENGTH} simbolių!")
    
    if not shared_validator.letters_numbers_only(username):
        raise exceptions.BadRequest("Vartotojo vardas negali turėti specialių simbolių!")
    

#Validate username to make sure email format is correct, email length is within specified bounds and email is clear of possible SQL queries
def validate_email(email: str):
    if not email:
        logging.warning("No email provided")
        raise exceptions.UnprocessableEntity("El. pašto adresas yra privalomas!")

    shared_validator.validate_sql_malicious_input(email)

    email_length = len(email)
    if email_length < config.MIN_EMAIL_LENGTH:
        logging.warning("Provided email is too short")
        raise exceptions.UnprocessableEntity(f"El. pašto adresas privalo turėti ne mažiau kaip {config.MIN_EMAIL_LENGTH} simbolius!")
    
    if email_length > config.MAX_EMAIL_LENGTH:
        logging.warning("Provided email is too long")
        raise exceptions.UnprocessableEntity(f"El. pašto adresas privalo turėti ne daugiau kaip {config.MAX_EMAIL_LENGTH} simbolių!")

    if not EMAIL_PATTERN.match(email):
        logging.warning(f"Provided email is invalid: {email}")
        raise exceptions.UnprocessableEntity("Neteisingas el. pašto adreso formatas!")


#Validate password to check if it is not too short or too long
def validate_password(password: str): 
    if not password: 
        logging.warning("No password provided") 
        raise exceptions.UnprocessableEntity("Slaptažodis yra privalomas!") 
    
    password_length = len(password)
    
    if password_length < config.MIN_PASSWORD_LENGTH: 
        logging.warning("Provided password is too short") 
        raise exceptions.UnprocessableEntity(f"Slaptažodis privalo turėti ne mažiau kaip {config.MIN_PASSWORD_LENGTH} simbolius!") 
    
    if password_length > config.MAX_PASSWORD_LENGTH:
        logging.warning("Provided password is too long") 
        raise exceptions.UnprocessableEntity(f"Slaptažodis privalo turėti ne daugiau kaip {config.MAX_PASSWORD_LENGTH} simbolių!") 
    

#Validate name to make sure it does not contain any symbols and check if it is not too long
def validate_name(first_name: str, last_name: str): 
    if not first_name: 
        logging.warning("No first name provided") 
        raise exceptions.UnprocessableEntity("Vardas yra privalomas!") 
    if not last_name:
        logging.warning("No last name provided") 
        raise exceptions.UnprocessableEntity("Pavardė yra privaloma!") 
    
    first_name_length = len(first_name)
    last_name_length = len(last_name)

    if first_name_length < config.MIN_USER_NAME_LENGTH:
        logging.warning("Provided first name is too short") 
        raise exceptions.UnprocessableEntity(f"Vardo lauko reikšmė privalo būti ne trumpesnė kaip {config.MIN_USER_NAME_LENGTH} simbolis!") 
    if last_name_length < config.MIN_USER_NAME_LENGTH:
        logging.warning("Provided last name is too short") 
        raise exceptions.UnprocessableEntity(f"Pavardės lauko reikšmė privalo būti ne trumpesnė kaip {config.MIN_USER_NAME_LENGTH} simbolis!") 
    
    if first_name_length > config.MAX_USER_NAME_LENGTH: 
        logging.warning("Provided first name is too long") 
        raise exceptions.UnprocessableEntity(f"Vardo lauko reikšmė privalo būti ne ilgesnė kaip {config.MAX_USER_NAME_LENGTH} simbolių!") 
    if last_name_length > config.MAX_USER_NAME_LENGTH: 
        logging.warning("Provided last name is too long") 
        raise exceptions.UnprocessableEntity(f"Pavardės lauko reikšmė privalo būti ne ilgesnė kaip {config.MAX_USER_NAME_LENGTH} simbolių!") 
    
    if NUMBER_PATTERN.search(first_name): 
        logging.warning("First name contains numbers") 
        raise exceptions.UnprocessableEntity("Vardo laukas negali turėti skaičių!") 
    if NUMBER_PATTERN.search(last_name): 
        logging.warning("Last name contains numbers") 
        raise exceptions.UnprocessableEntity("Pavardės laukas negali turėti skaičių!") 
    
    if NAME_PATTERN.search(first_name): 
        logging.warning("First name contains special symbols") 
        raise exceptions.UnprocessableEntity("Vardo laukas negali turėti specialių simbolių!") 
    if NAME_PATTERN.search(last_name): 
        logging.warning("Last name contains special symbols") 
        raise exceptions.UnprocessableEntity("Pavardės laukas negali turėti specialių simbolių!") 