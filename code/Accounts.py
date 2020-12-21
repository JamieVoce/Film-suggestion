import csv
import os
import hashlib
import Password_validation

script_dir = os.path.dirname(__file__)  # Script directory
script_dir, x = script_dir.rsplit('\\', 1) #This line won't run correctly when running this file but will run when running the main file
accounts_file_path = os.path.join(script_dir, 'user_data.csv')


def writing_account(signup_username, signup_password):
    if os.path.isfile(accounts_file_path): #If the file exists, append new account to the file
        with open(accounts_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([signup_username, signup_password])
            
    else: #If the file doesn't exist, create the file
        with open(accounts_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Password", "Watched films"])
            writer.writerow([signup_username, signup_password])


def reading_account(login_username, login_password):
    if os.path.isfile(accounts_file_path):
        with open(accounts_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',') #Read each line of the user_data csv
            next(csv_reader) #Skip the first line because it's just the headings for the columns
            for row in csv_reader:
                if row[0] == login_username and row[1] == login_password:
                    return row


def updating_account_data(account, likes_to_save):
    lines_to_write_back = []
    with open(accounts_file_path, 'r', newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in reader:
            if row[0] == account[0] and row[1] == account[1]:
                string_of_likes = ""
                for like in range(len(likes_to_save)-1):
                    string_of_likes += str(likes_to_save[like]) + ","
                string_of_likes += str(likes_to_save[-1])
                lines_to_write_back.append((row[0], row[1], string_of_likes))
            else:
                lines_to_write_back.append((row))

    with open(accounts_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in lines_to_write_back:
            try: #This is needed because some films may have no likes yet
                data = line[2]
            except:
                data = ""
            writer.writerow([line[0], line[1], data])
    quit()

    
def hashing(data_to_encrypt):
    SALT = "AbX2f8Z&1SVFHUB4UZPW"
    plus_salt = data_to_encrypt + SALT
    hashed_data = hashlib.sha256((plus_salt).encode()).hexdigest()
    return hashed_data

    
def login():
    login_username = hashing(input("Username: "))
    login_password = hashing(input("Password: "))
    account_found = reading_account(login_username, login_password)
    if account_found != None:
        return account_found


def signup():
    checks_passed = False
    while not checks_passed:
        signup_username = hashing(input("Username: "))
        unhashed_password =  input("Password: ")
        checks_passed = Password_validation.run_checks(unhashed_password) #Password validation
    hashed_password = hashing(unhashed_password)
    writing_account(signup_username, hashed_password)


def main_menu():
    while 1:
        answer = input("Do you want to login or signup?")
        if answer.lower() == "signup":
            signup()
        elif answer.lower() == "login":
            account_data = login()
            if account_data != None:
                return account_data
            else:
                print("Invalid account details")
        else:
            print("That was not a valid option")