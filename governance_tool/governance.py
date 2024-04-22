import json
import pickle
import random
from datetime import datetime

custodians_list = []
global_user_id = ""
JSON_PATH = 'data.json'
SEREALIZED_PATH = 'serialized.pkl'

#Function to generate random id with a given prefix
def generate_random_id(prefix):
    #Generate a random ID with a prefix.
    return f"{prefix}_{random.randint(1000, 9999)}"

#Function to generate a dataset information
def generate_dataset():
    dataset_id = generate_random_id("dataset")
    dataset_location = generate_random_id("location")
    dataset_hospital = generate_random_id("hospital")
    dataset_class = generate_random_id("class")
    resource_id = generate_random_id("resource")
    dataset_uri = f"/resources/{resource_id}"
    dataset_status = generate_random_status(resource_creation=True)
    dataset_date = generate_random_timestamp()
    dataset = {
                "id": dataset_id, 
                "location": dataset_location,
                "hospital": dataset_hospital,
                "class": dataset_class,
                "uri": dataset_uri,
                "status": dataset_status,
                "date": dataset_date
                }
    return dataset

#Function to generate a list of datasets based on a given number
def generate_dataset_list(number_of_datasets):
    list = []
    for i in range(number_of_datasets):
        list.append(generate_dataset())
    return list

#Function to generate a custodian information (id and list of datasets in control)
def generate_custodian(number_of_datasets):
    custodian_id = generate_random_id('custodian')
    list_datasets = generate_dataset_list(number_of_datasets)
    custodian = {
        "id": custodian_id,
        "datasets_list": list_datasets
    }
    return custodian

#Function to generate a list of custodians based on a given number
def generate_custodians_list(number_custodians):
    list = []
    for i in range(number_custodians):
        list.append(generate_custodian(random.randint(1,10)))
    return list

#Function to check the id of a dataset. Returns 1 if dataset exists and 0 if not
def check_dataset_id(input):
    global custodians_list
    for custodian in custodians_list:
        datasets = custodian["datasets_list"]
        for dataset in datasets:
            if input == dataset["id"]:
                return 1
    return 0

#Function to print info of all datasets available 
def get_all_datasets():
    global custodians_list
    data = load_data()
    auditing_service = data["ResourceCreation"]
    for audit in auditing_service:
        print(audit)

#Function to print the status of all datasets in auditingservice (to view as custodian)
def get_all_datasets_status():
    global custodians_list
    data = load_data()
    auditing_service = data["AuditingService"]
    for audit in auditing_service:
        targ_resources = audit["TargetResources"]
        print("Dataset ID: ", targ_resources["DatasetID"], " | Data Custodian: ", audit["DataCustodian"], "| Data User: ", audit["DataUser"], " | Status: ", audit["Status"])

#Function to print custodians and associated datasets
def get_all_custodians():
    global custodians_list
    for custodian in custodians_list:
        print("Custodian: ", custodian["id"])
        datasets = custodian["datasets_list"]
        print("Associated Datasets: ")
        for dataset in datasets:
            print(" - Dataset ID: ", dataset["id"])
            print()

#Function to load json saved data to structure. CHANGE PATH
def load_data():
    with open(JSON_PATH, 'r') as file:
        # Load the entire JSON content of the file into a Python dictionary
        data_read = json.load(file)
        return data_read
    
#Functions to request permission for a dataset (to use as data user)
def request_permission(dataset_id):
    global custodians_list, global_user_id
    for custodian in custodians_list:
        datasets = custodian["datasets_list"]
        for dataset in datasets:
            if dataset_id == dataset["id"]:
                uri = dataset["uri"]
                custodian_id = custodian["id"]
                data = {
                    'DataUser': global_user_id,
                    'DataCustodian': custodian_id,
                    'TargetResources': {
                        'DatasetID': dataset_id,
                        'Location': dataset["location"],
                        'HospitalID': dataset["hospital"],
                        'ResourceClass': dataset["class"],
                        'URI': f"/resources/{uri}"
                    },
                    'Date': generate_random_timestamp(),
                    'Status': "Requested"
                }
                data_read = load_data()
                data_read["AuditingService"].append(data)
                save_data(data_read)

                return 1
    return 0

#Function for the menu for the data users. Allows to view all permission status of current user on datasets and request permission for a dataset (use as data user)
def datasets_menu():
    global global_user_id
    while True:
        print("\n----- Datasets Menu -----")
        print("----- Actions -----")
        print("1. Request Permission to Dataset")
        print("2. Check Permission Status")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            aux = 0
            while aux == 0:
                dataset_id = input("Which dataset? (type the id or 0 to leave): ")
                if dataset_id == 0:
                    aux += 2
                check = check_dataset_id(dataset_id)
                if check == 1:
                    print("Dataset id correctly typed.")
                    aux += 1
                else:
                    print("The dataset typed does not exist. Please select a dataset that exists or type 0 to leave.") 
            if aux == 2:
                return -1
            else:
                request_result = request_permission(dataset_id)
                if request_result == 1:
                    print("Request made for dataset ", dataset_id)
                else:
                    print("Request not made for dataset ", dataset_id)

        elif choice == '2':
            data_read = load_data()
            audit_service = data_read["AuditingService"]
            aux = 0
            for permission in audit_service:
                target_resources = permission["TargetResources"]
                if permission["DataUser"] == global_user_id:
                    print("DatasetID:", target_resources["DatasetID"], "Permission Status: ", permission["Status"])
                    aux+=1
                    #break
            if aux == 0:
                print("Not able to check status of permission.")
        elif choice == '3':
                print("Exiting the program.")
                break
        else:
            print("Invalid choice. Please try again.")

#Function to change the status of a dataset (as custodian - grant or revoke permission)
def change_dataset_status():
    aux = 0
    while aux == 0:
        data = load_data()
        auditing_service = data["AuditingService"]
        choice = input("Dataset ID to change status: ")
        choice3 = input("User to change dataset status (permission): ")
        for audit in auditing_service:
            targ_resources = audit["TargetResources"]
            if targ_resources["DatasetID"] == choice and audit["DataUser"]==choice3:
                strings_list = ["Requested", "Granted", "Revoked"]
                # String to remove
                string_to_remove = audit["Status"]
                # Removing string from the list using a loop
                new_list = [s for s in strings_list if s != string_to_remove]
                for i in range(len(new_list)):
                    print("Type ", i, " to change for status: ", new_list[i])
                choice2 = input("Status to change: ")
                for i in range(len(new_list)):
                    if int(choice2) == int(i):
                        print("Status Changed to: ", new_list[i])
                        audit["Status"] = new_list[i]
                        save_data(data)
                        aux += 1 
        if aux == 0:
            print("Wrong type")
        
#Function to create a resource  (dataset) - automatically creates, no manual intervention with random values
def create_resource():
    data = load_data()
    resource_creation = data["ResourceCreation"]
    new_data = {
            'DataCustodian': generate_random_id('custodian'),
            'DatasetID': generate_random_id("dataset"), 
            'Location': generate_random_id('location'),
            'HospitalID': generate_random_id('hospital'),
            'ResourceClass': generate_random_id('class'),
            'URI': f"/resources/{generate_random_id('resource')}",
            'Status': generate_random_status(resource_creation=True),
            'Date': generate_random_timestamp()
    }
    print("Resource ", new_data, "created")
    resource_creation.append(new_data)
    save_data(data)

#Function to print all datasets (resources) 
def get_all_resources():
    data = load_data()
    resource_creation = data["ResourceCreation"]
    for resource in resource_creation:
        print("Resource: ", resource)
        print()

#Function to change the status of a dataset (released changed or removed) - as data custodian
def change_resource():
    data = load_data()
    resource_creation = data["ResourceCreation"]
    get_all_resources()
    aux = 0
    while aux == 0:
        choice = input("Type the resource uri to change: ")
        for resource in resource_creation:
            resource_options = resource["DatasetID"]
            if resource["URI"] == choice:
                strings_list = ["Released", "Changed", "Removed"]
                # String to remove
                string_to_remove = resource["Status"]
                # Removing string from the list using a loop
                new_list = [s for s in strings_list if s != string_to_remove]
                for i in range(len(new_list)):
                    print("Type ", i, " to change for status: ", new_list[i])
                choice2 = input("Status to change: ")
                for i in range(len(new_list)):
                    if int(choice2) == int(i):
                        print("Status Changed to: ", new_list[i])
                        resource["Status"] = new_list[i]
                        save_data(data)
                        aux += 1
        if aux == 0:
            print("Wrong type") 

#Function to check existent data users
def check_data_users():
    data = load_data()
    auditing_service = data["AuditingService"]
    list_users = []
    for audit in auditing_service:
        data_user = audit["DataUser"]
        if data_user not in list_users:
            list_users.append(data_user)
    print("Users: ", list_users)

#Function to check existent data operation rules
def check_data_operation_rules():
    data = load_data()
    data_rules = data["DataOperationRules"]
    for rule in data_rules:
        print(rule)

#Function to create a data operation rule (automatically, no manual intervention with random values)
def create_data_rules():
    data = load_data()
    data_rules = data["DataOperationRules"]
    new_data = {
            'DataCustodian': generate_random_id('custodian'),
            'DatasetID': generate_random_id('dataset'),
            'DataUser': generate_random_id('user'),
            'CreationDate': generate_random_timestamp(),
            'ExpirationDate': generate_random_timestamp(),
            'Rules': random.choice(['always grant', 'conditional access', "never grant"]),
            'RuleID': generate_random_id("rule")
    }
    data_rules.append(new_data)
    save_data(data)

#Function to change a data operation rule (as always grant, never grant or conditional access)
def change_data_rules():
    data = load_data()
    data_rules = data["DataOperationRules"]
    #get_all_resources()
    aux = 0
    while aux == 0:
        choice = input("Type the RuleID: ")
        for rule in data_rules:
            #resource_options = resource["DatasetID"]
            if rule["RuleID"] == choice:
                strings_list = ["always grant", "conditional access", "never grant"]
                # String to remove
                string_to_remove = rule["Rules"]
                # Removing string from the list 
                new_list = [s for s in strings_list if s != string_to_remove]
                for i in range(len(new_list)):
                    print("Type ", i, " to change for status: ", new_list[i])
                choice2 = input("Status to change: ")
                for i in range(len(new_list)):
                    if int(choice2) == int(i):
                        print("Status Changed to: ", new_list[i])
                        rule["Rules"] = new_list[i]
                        save_data(data)
                        aux += 1
        if aux == 0:
            print("Wrong type") 

#Function to execute the menu when using as custodian
def custodians_menu():
    global global_user_id
    while True:
        print("\n----- Custodians Menu ------")
        print("----- Actions -----")
        print("1. Check dataset status")
        print("2. Change dataset status")
        print("3. Create Resource(dataset)")
        print("4. Change Resource(dataset)")
        print("5. Check data users")
        print("6. Check Data operation Rules")
        print("7. Create Data Operation Rules")
        print("8. Change data operation Rules")
        print("9. Exit")
        choice = input("Enter your choice (1-9): ")
        if choice == '1':
            #Check dataset status
            get_all_datasets_status()
        elif choice == '2':
            #Change dataset status
            change_dataset_status()
        elif choice == '3':
            #Create resource
            create_resource()
        elif choice == '4':
            #Change resource
            change_resource()
        elif choice == '5':
            #Check data users
            check_data_users()
        elif choice == '6':
            #Check data operation rules
            check_data_operation_rules()
        elif choice == '7':
            #Create data operation rules
            create_data_rules()
        elif choice == '8':
            #Change data operation rules
            change_data_rules()
        elif choice == '9':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

#Function to generate random timestamp
def generate_random_timestamp():
    #Generate a random timestamp within the last year.
    now = datetime.now()
    timestamp = now.timestamp() - random.randint(0, 31536000)  # 365 days in seconds
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

#Function to generate random status for the auditing service ("granted, revoked, or requested") and for the resource creation (datasets), as released, removed, changed
def generate_random_status(audit=False, resource_creation=False):
    #Generate random status based on the context.
    if audit:
        return random.choice(['Requested', 'Granted', 'Revoked'])
    elif resource_creation:
        return random.choice(['Released', 'Changed', 'Removed'])
    return None

#Function to generate random data data - currently not being used
def generate_data():
    #Generate random data for all the required fields.
    data = {
        'AuditingService': [
            {
            'DataUser': generate_random_id('user'),
            'DataCustodian': generate_random_id('custodian'),
            'TargetResources': {
                'DatasetID': generate_random_id('dataset'),
                'Location': generate_random_id('location'),
                'HospitalID': generate_random_id('hospital'),
                'ResourceClass': generate_random_id('class'),
                'URI': f"/resources/{generate_random_id('resource')}"
            },
            'Date': generate_random_timestamp(),
            'Status': generate_random_status(audit=True)
            }
        ],
        'ResourceCreation': [
            {
            'DataCustodian': generate_random_id('custodian'),
            'DatasetID': generate_random_id("dataset"),
            'Location': generate_random_id('location'),
            'HospitalID': generate_random_id('hospital'),
            'ResourceClass': generate_random_id('class'),
            'URI': f"/resources/{generate_random_id('resource')}",
            'Status': generate_random_status(resource_creation=True),
            'Date': generate_random_timestamp()
            }
        ],
        'DataOperationRules': [
            {
            'DataCustodian': generate_random_id('custodian'),
            'DatasetID': generate_random_id('dataset'),
            'DataUser': generate_random_id('user'),
            'CreationDate': generate_random_timestamp(),
            'ExpirationDate': generate_random_timestamp(),
            'Rules': random.choice(['always grant', 'conditional access', "never grant"]),
            'RuleID': generate_random_id("rule")
            }
        ]
    }
    return data

#Function to save data in json file and pkl (serialize). CHANGE PATH
def save_data(data, json_path=JSON_PATH, serialized_path=SEREALIZED_PATH):
    # Save as JSON
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    # Serialize and save
    with open(serialized_path, 'wb') as serialized_file:
        pickle.dump(data, serialized_file)

#Function to feed json data "structures" with previously generated random data
def feed_data():
    data_read = load_data()
    global custodians_list
    for custodian in custodians_list:
        datasets = custodian["datasets_list"]
        for dataset in datasets:
            custodian_id = custodian["id"]
            uri = dataset["uri"]
            data = {
                    'DataUser': generate_random_id("user"),
                    'DataCustodian': custodian_id,
                    'TargetResources': {
                        'DatasetID': dataset["id"],
                        'Location': dataset["location"],
                        'HospitalID': dataset["hospital"],
                        'ResourceClass': dataset["class"],
                        'URI': f"/resources/{uri}"
                    },
                    'Date': generate_random_timestamp(),
                    'Status': generate_random_status(audit=True)
            }
            
            data_read["AuditingService"].append(data)
    
    resource_creation = {
                    'DataCustodian': generate_random_id('custodian'),
                    'DatasetID': generate_random_id("dataset"),
                    'Location': generate_random_id('location'),
                    'HospitalID': generate_random_id('hospital'),
                    'ResourceClass': generate_random_id('class'),
                    'URI': f"/resources/{generate_random_id('resource')}",
                    'Status': generate_random_status(resource_creation=True),
                    'Date': generate_random_timestamp()
                    }
                            
    data_read["ResourceCreation"].append(resource_creation)
    data_operation_rules = {
            'DataCustodian': generate_random_id('custodian'),
            'DatasetID': generate_random_id('dataset'),
            'DataUser': generate_random_id('user'),
            'CreationDate': generate_random_timestamp(),
            'ExpirationDate': generate_random_timestamp(),
            'Rules': random.choice(['always grant', 'conditional access', "never grant"]),
            'RuleID': generate_random_id("rule")
            }
    data_read["DataOperationRules"].append(data_operation_rules)
    for custodian in custodians_list:
        datasets = custodian["datasets_list"]
        for dataset in datasets:
            dataset_uri = dataset["uri"]
            resource_creation = {
                'DataCustodian': custodian["id"],
                'DatasetID': dataset["id"],
                'Location': dataset["location"],
                'HospitalID': dataset["hospital"],
                'ResourceClass': dataset["class"],
                'URI': dataset_uri,
                'Status': dataset["status"],
                'Date': dataset["date"]
                }
                            
            data_read["ResourceCreation"].append(resource_creation)
        
    save_data(data_read)

#Function to generate empty data for the jsons (initial)
def generate_base_data():
    data = {
        'AuditingService': [],
        'ResourceCreation': [],
        'DataOperationRules': []
    }
    return data

#Function to print the main menu (1 as data users and 2 as data custodians)
def show_menu():
    print("\n----- Main Menu -----")
    print("1. Show All Datasets")
    print("2. Show All Custodians")
    print("3. Exit")

#Function main. generates a random id to use if simulate data user. initiates data and saves on the json file (random data)
#Choosing 1 on the menu simulates a data user. It has an id and can request permission to access previously random generated datasets
#Chossing 2 on the menu simulates a data custodian. It can check the status of datasets (granted, revoked, requested), change the status of the datasets (requested -> granted/revoked for ex.), create resources (datasets, automatically and random values generated),
#change the status of the resources (released, removed, changed), check current data users (with past or present access to datasets), check data operation rules, create operation rules, and change the rules (always grant, never grant, conditional access).
#Purpose of check data structure and jsons, variables, flow of interactions, etc. On some "menus", not possible to exit without perform action (use ctrl+c). Json data saved on a data.json file (change path on the save_data function and load_data)
#On the Json, messages based on permissions and the auditing service are being saved under the "AuditingService", resources under "ResourceCreation", and data operation rules under "DataOperationRules".
def main():
    global custodians_list, global_user_id
    custodians_list = generate_custodians_list(3)
    user_id = generate_random_id("user")
    global_user_id = user_id
    print("User Logged with id: ", user_id)
    data_to_save = generate_base_data()
    save_data(data_to_save)
    feed_data()
    while True:
        show_menu()
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            #Show Datasets
            get_all_datasets()
            datasets_menu()
        elif choice == '2':
            #Show Custodians
            get_all_custodians()
            custodians_menu()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()