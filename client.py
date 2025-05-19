#client.py
import xmlrpc.client
import json

def biweeklyIncomeCalculator():
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

def authenticateUser(user_entered, pass_entered):
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

def main():
    #Connect with the Server application
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    print("=================================")
    print("=== Welcome to Tax Calculator ===")
    print("=================================\n")

    #Login Menu, inputs the username and password
    username = input("Username: ")
    password = input("Password: ")
    authenticate = authenticateUser(username, password) #Verifies the credentials

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
                    income_pairs = biweeklyIncomeCalculator() #Get the biweekly income
                    #print(income_pairs) #Debugging
                    break #Exits the while loop of getting TFN

                #TFN entered are 8 digit numbers 
                if tfn.isdigit() and len(tfn) == 8:
                    has_TFN = True
                    break
                else: #Invalid format of TFN, e.g. characters, more or less than 8 digits
                    print("Invalid TFN format. It must be 8 digits or -1 if not available")
                
            #User enters PHIC
            while True:
                try:
                    have_PHIC = input("\nDo you have a Private Health Insurance Cover? (y/n): ").lower()
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
                    print(f"Error: {e}")

            if has_TFN: #User does have a TFN, set default of biweekly pair value to (0,0)
                income_pairs.append((0,0))
            
            data = [income_pairs, have_PHIC, username] #Combines biweeklypairs, PHIC, and username
            #print(data) #Debugging
            try:
                #Sends the result to server-side and recevies the value to 'result'
                result = proxy.get_data(data)

                print("\n\n==========================")
                print("=== Tax Summary Report ===")
                print("==========================\n")
                #If the value received is a string (Error message)
                if type(result) is str:
                    print(result) #Print the message
                else: #If its a list
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
            except Exception as e:
                print(f"Error {e}")
        else: #Unauthenticated user, invalid credentials
            print("Authentication failed!")
    else: #Will only work first time running the application
        print(authenticate)

if __name__ == "__main__":
    main()
