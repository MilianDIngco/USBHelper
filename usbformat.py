import os
import time
import win32api
import win32file
import shutil
"""
AUTHOR - MILIAN INGCO
DATE - 7/18
DESCRIPTION: 
    Edits all new drives put into the computer and adds folders. 

"""

#Enter list of instructions

"""
CREATE - creates an item in a destination
parameters CREATE [item type] [destination] [name rule]

item types include
 - FOLDER
 - FILE

 DELETE - deletes an item given a path
 parameters DELETE [item type] [destination] 

 item types include 
 - FOLDER
 - FILE


defines a rule for names to be created
parameters [name of the rule] [rules] ...

$ - indicates user will enter text (only includes alphabetical characters)
"" - regular string 


example: 
CREATE FOLDER {folder destination (if left blank, will just place at root in that drive)}

"""

#stuff i dont wanna see
name_rule_text = "______________________________________\nName rules follow the format: [name of the rule CANNOT INCLUDE SPACES] [rules]\n - $ indicates user will replace with text\n - \"\" is normal text, can include spaces and alphabetical characters only\nEverything after the name of the rule will be considered the rules\nEnter \"done\" to finish\n______________________________________\n"

instruction_text = """---------------------------------------
Instruction functions include 
 - CREATE
 - DELETE

 CREATE is used to create any item in a specific destination and follows these parameters
 CREATE [item type] [destination] [name rule name]
 The destination string must not include spaces
 These instructions will be run for each NEW drive put into the computer

 DELETE is used to delete any item in a specific destination using these parameters
 DELETE [item type] [destination]
---------------------------------------"""

#functions
def create_name(rule: str) -> str:
    final_string = ""
    in_quote = -1
    for char in rule:
        #check for $
        if char == '$':
            user_input = input("Enter input: ")
            final_string = final_string + user_input
        if char == '\"':
            in_quote *= -1
            continue
        if in_quote == 1:
            final_string = final_string + char

    return final_string

def create_folder(path: str, folder_name: str):
    path = os.path.join(path, folder_name)
    try:
        os.makedirs(path, exist_ok=True)
        print("Successfully created")
    except OSError as error:
        print("Directory couldn't be created")

def create_file(path: str, file_name: str):
    path = os.path.join(path, file_name)
    try:
        file = open(path, 'w')
        file.close()
        print("Successfully created")
    except Exception as e:
        print("An error has occured while deleting the file")

def delete_folder(path: str):
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
            print("Successfully deleted")
        else:
            print("DNE")
    except Exception as e:
        print("An error has occured while deleting the folder")

def delete_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
            print("Successfully deleted")
        else:
            print("DNE")
    except Exception as e:
        print("An error has occured while deleting the folder")

#get all drives that shouldn't be changed
current_drives = win32api.GetLogicalDriveStrings()
current_drives = current_drives.split('\000')[:-1]

print(current_drives)

#get list of naming rules
name_rules = {} # variable name : rule string 

print(name_rule_text)
name_user_input = input("Enter naming rule: \n")
while(name_user_input != "done"):
    if len(name_user_input.split(maxsplit=1)) < 2:
        print("Enter name rules properly\n")
        name_user_input = input()
        continue
    input_list = name_user_input.split(maxsplit=1)
    name_rules[input_list[0]] = input_list[1]
    name_user_input = input()

#get list of instruction_user_input
instruction_list = [] 

print(instruction_text)
instruction_user_input = input("Enter instructions: \n")
while(instruction_user_input != "done"):
    input_list = instruction_user_input.split()
    instruction_list.append(input_list)
    instruction_user_input = input()

print(name_rules)
print(instruction_list)
    
while True:
    time.sleep(1) #checks each second for a new drive
    check_drives = (win32api.GetLogicalDriveStrings()).split('\000')[:-1]
    check_drives = [item for item in check_drives if item not in current_drives]
    if len(check_drives) < 1:
        continue

    for drive in check_drives:
        for instruction in instruction_list:
            if instruction[0].upper() == "CREATE":
                path = os.path.join(drive, instruction[2])
                if instruction[1].upper() == "FOLDER":
                    create_folder(path, create_name(name_rules[instruction[3]]))
                elif instruction[1].upper() == "FILE":
                    create_file(path, create_name(name_rules[instruction[3]]))
            elif instruction[0].upper() == "DELETE":
                if instruction[1].upper() == "FOLDER":
                    path = os.path.join(drive, " ".join(instruction[2:]))
                    delete_folder(path)
                elif instruction[1].upper() == "FILE":
                    path = os.path.join(drive, " ".join(instruction[2:]))
                    delete_file(path)
    while len(check_drives) > 0:
        time.sleep(1) #checks each second for a new drive
        check_drives = (win32api.GetLogicalDriveStrings()).split('\000')[:-1]
        check_drives = [item for item in check_drives if item not in current_drives]
        
    

