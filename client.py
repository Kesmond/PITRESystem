#client.py
import xmlrpc.client
import json

def biweekly_income_calculator():
    #Function to input biweekly pairs
    print("\nEnter up to 26 biweekly income and tax withheld (e.g. '1000 100')")
    tax_pairs = []
    sum_income = 0
    week = 1
    while week <= 26:
        #User inputs biweekly pair
        weekly_pair = input(f"Enter biweekly income (Week {week}) or 'done' to finish: ")

        if weekly_pair.lower() == 'done': #If it enters 'done' to exit
            #Make sure values aren't (0,0)
            if sum_income > 0:
                print("Exited by user.")
                break
            else: #Prints an error message
                print("Income and tax can't be zero.")
                continue

        try:
            income, tax = map(float, weekly_pair.split())
            if income < 0 or tax < 0: #Numbers entered must be positive numbers
                print("Values cannot be negative. Please try again.")
                continue
            elif tax >= income: #Income must be higher than tax
                print("Please enter the right amount.")
                continue

            sum_income = sum_income + income #Used for ensuring first if function
            tax_pairs.append((income,tax))
            week += 1
        except ValueError: #Captures any invalid input format
            print("Invalid input. Please enter two numbers, separated by space.")

    return tax_pairs

def authenticate_user(user_entered, pass_entered):
    #Function to authenticate users during first login
    try:
        #Get the JSON file and load its values
        with open("userauthentication.json") as f:
            users = json.load(f)
    except:
        #If JSON file doesn't exists, creates a new database
        #This will only happen on the first time running the application
        users = {
            "240704": "password123",
            "123456": "admin123",
            "987654": "user123"
        }
        #Store the values to the database
        with open("userauthentication.json", "w") as f:
            json.dump(users, f)
        return "Database isn't found. Created a new database."
    
    #If username and password entered matches the database
    if user_entered in users and users[user_entered] == pass_entered:
        return True #User verified
    else:
        return False #User unverified

#Get credentials for second level authentication
def get_user_information(): #CASE SENSITIVE SINCE IT IS PERSONAL INFORMATION
    print("\n=== Personal Details ===")
    while True:
        f_name = input("First name: ").strip()
        if not f_name: #Must enter first name
            print("First name required.")
            continue
        break

    while True:
        l_name = input("Last name: ").strip()
        if not l_name: #Must enter last name
            print("Last name required.")
            continue
        break

    while True:
        email = input("Email: ").strip()
        if not email: #Must enter email
            print("Email required.")
            continue
        break

    return { #Return values
        'f_name': f_name,
        'l_name': l_name,
        'email': email
    }

def main():
    #Connect with the Server application
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    print("=================================")
    print("=== Welcome to Tax Calculator ===")
    print("=================================\n")

    #Login Menu, inputs the username and password
    username = input("Username: ")
    password = input("Password: ")
    authenticate = authenticate_user(username, password) #Verifies the credentials

    if type(authenticate) is bool:
        if authenticate: #Verified user
            income_pairs = []
            has_TFN = False
            print("\n=== Welcome! ===\n")
            print("Please enter your 8 digit TFN number! (-1 if you don't have)")
            
            #User enters TFN
            while True:
                tfn = input("Enter your Tax File Number (TFN): ")
                if tfn == "-1": #Doesn't have TFN
                    tfn = -1
                    has_TFN = False
                    income_pairs = biweekly_income_calculator() #Get the biweekly income
                    #print(income_pairs) #DEBUG
                    break #Exits the while loop of getting TFN

                #TFN entered are 8 digit numbers
                if tfn.isdigit() and len(tfn) == 8:
                    has_TFN = True
                    user_information = get_user_information()
                    break
                else: #Invalid format of TFN, e.g. characters, more or less than 8 digits
                    print("Invalid TFN format. It must be 8 digits or -1 if not available")
                
            #User enters PHIC
            while True:
                try:
                    have_PHIC = input("\nDo you have a Private Health Insurance Cover? (y/n): ").lower().strip()
                    if have_PHIC == 'y': #Does have PHIC
                        have_PHIC = True
                        break
                    elif have_PHIC == 'n': #Does NOT have PHIC
                        have_PHIC = False
                        break
                    else: #Any other values
                        raise ValueError("Invalid input. Please enter 'y' or 'n'.")
                        break
                except ValueError as e:
                    print(f"Client 1 Error: {e}")

            if has_TFN: #User does have a TFN, set default of biweekly pair value to (0,0)
                income_pairs.append((0,0))
            else: #If user DOESN'T have TFN, personal information isn't needed
                user_information = {
                    'f_name': 'N/A',
                    'l_name': 'N/A',
                    'email': 'N/A',
                }
            
            data = { #Stores all information to be sent to server application
                'income_pairs': income_pairs,
                'insurance': have_PHIC,
                'user_id': username,
                'tfn': tfn,
                'user_information': user_information
            }
            try:
                #Sends the result to server-side and recevies the value to 'result'
                result = proxy.get_data(data)
                print("")

                #If the value received is a string (Error message)
                if type(result) is str:
                    print(result) #Print the message
                else: #If its a list
                    print("\n==========================")
                    print("=== Tax Summary Report ===")
                    print("==========================\n")
                    #Print the values
                    print("ID:", result[0])
                    if result[1]:
                        print("TFN:", tfn)
                    else:
                        print("No TFN")
                    print("")
                    print(f"Annual Taxable Income: ${result[2]:.2f}")
                    print(f"Total Tax Witheld: ${result[3]:.2f}")
                    print(f"Total net-income: ${result[4]:.2f}")
                    print(f"Total tax:: ${result[6]:.2f}")
                    print("")
                    if result[5] >= 0:
                        print(f"Estimated tax refund of: ${result[5]:.2f}")
                    elif result[5] < 0:
                        print(f"Estimated tax amount of: ${result[5]*-1:.2f} owing to the ATO")
            except ConnectionError: #Server 1 is offline
                print("Client cannot connect to server 1")
            except Exception as e:
                print(f"Client 2 Error {e}")
        else: #Unauthenticated user, invalid credentials
            print("Authentication failed!")
    else: #Will only work first time running the application
        print(authenticate)

if __name__ == "__main__":
    main()
