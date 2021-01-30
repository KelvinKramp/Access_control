import re
from cryptography.fernet import Fernet
import keyring
import os

# DEFINE FUNCTIONS FOR ENCRYPTING FROM https://devqa.io/encrypt-decrypt-data-python/
def load_key():
    """
    Load the previously generated key
    """
    key = keyring.get_password("system", "username")
    return key

def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    return encrypted_message

def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    return decrypted_message.decode()

# DEFINE FUNCTIONS FOR PASSWORD CHECK IN FILES https://thispointer.com/python-search-strings-in-a-file-and-get-line-numbers-of-lines-containing-the-string/
def check_if_password_in_file(file, password):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if password in line:
                print("PASSWORD FOUND IN ONE OF THE FILES!!")
                print("path file =", file)
                password_files.append(file)


# RUN SCRIPT
if __name__ == "__main__":
    # IF NO SECRETS.JSON FILE THEN PLACE PASSWORDS OVER HERE AS A LIST
    # FOR EXAMPLE: passwords=['password1', "password2"] AND THEN REMOVE SECRETS.JSON OPEN FILE BLOCKING
    # AND PASSWORD DECRYPTION BLOCK

    # OPEN FILE SECRETS.JSON
    with open('secrets.json') as f:
        lines = f.read()

    # PASSWORD DECRYPTION
    encrypted_passwords = re.findall(r'[g][A][A].+', lines)
    passwords = []
    for encrypted_password in encrypted_passwords:
        encrypted_password = encrypted_password[:-1]
        password = decrypt_message(encrypted_password.encode('utf-8'))
        passwords.append(password)

    # RECURSE OVER FILES AND LOOK FOR PASSWORD IN FILES, PLACE THIS FILE IN MAINDIRECTORY FROM WHICH YOU WANT TO SEARCH RECURSIVELY
    directory = r'./'
    password_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # FOLLOWING LINE IS ADDITIONAL IF STATMENT FOR ONLY SEARCHING IN PYTHON FILES, REMOVE THIS IF YOU WANT TO SEARCH IN ALL FILES
            if file.endswith(".py"):
                path = os.path.join(root, file)
                print(path)
                for password in passwords:
                    check_if_password_in_file(path, password)
        else:
            continue
    print("files checked")
    print("list of files with passwords =", password_files)
