#client.py
import xmlrpc.client

def biweeklyIncomeCalculator():
    print("\nEnter up to 26 biweekly income and tax withheld (e.g. '1000 100')")
    tax_pairs = []
    sum_income = 0
    week = 1
    while week <= 26:
        weekly_pair = input(f"Enter biweekly income (Week {week}) or 'done' to finish: ")

        if weekly_pair.lower() == 'done':
            if sum_income > 0:
                print("Exited by user.")
                break
            else:
                print("Income and tax can't be zero.")
                continue

        try:
            income, tax = map(float, weekly_pair.split())
            if income < 0 or tax < 0:
                print("Values cannot be negative. Please try again.")
                continue
            elif tax >= income:
                print("Please enter the right amount.")
                continue

            sum_income = sum_income + income
            tax_pairs.append((income,tax))
            week += 1
        except ValueError:
            print("Invalid input. Please enter two numbers, separated by space.")

    return tax_pairs


def main():
    #Authentication
    #ID 6 digit and password
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
    #username = input("Username: ")
    #password = input("Password: ")
    username = 123456
    password = "admin"

    if username == 123456 and password == 'admin':
        #Implementation
        income_pairs = []
        has_TFN = False
        print("\nWelcome User!")
        print("Please enter your 8 digit TFN number! (-1 if you don't have)")
        
        while True:
            tfn = input("Enter your Tax File Number (TFN): ")
            if tfn == "-1":
                tfn = -1
                has_TFN = False
                income_pairs = biweeklyIncomeCalculator()
                #print(income_pairs)
                break

            if tfn.isdigit() and len(tfn) == 8:
                has_TFN = True
                break
            else:
                print("Invalid TFN format. It must be 8 digits or -1 if not available")
            
        while True:
            try:
                have_PHIC = input("\nDo you have a Private Health Insurance Cover? (y/n): ").lower()
                if have_PHIC == 'y':
                    have_PHIC = True
                    break
                elif have_PHIC == 'n':
                    have_PHIC = False
                    break
                else:
                    raise ValueError("Invalid input. Please enter 'y' or 'n'.")
                    break
            except ValueError as e:
                print(f"Error: {e}")

        if has_TFN:
            income_pairs.append((0,0))
        
        data = [income_pairs, have_PHIC, username]
        print(data)
        try:
            result = proxy.get_data(data)

            print("")
            if type(result) is str:
                print(result)
            else:
                print("ID:", result[0])
                if result[1]:
                    print("TFN:", tfn)
                else:
                    print("No TFN")
                print("")
                print("Annual Taxable Income:", result[2])
                print("Total Tax Witheld:", result[3])
                print("Total net-income:", result[4])
                print("Total tax:", result[6])
                print("")
                if result[5] >= 0:
                    print("Estimated tax refund of:", result[5])
                elif result[5] < 0:
                    print(f"Estimated tax amount of ${result[5]*-1} owing to the ATO")
        except Exception as e:
            print(f"Error {e}")
    else:
        print("Authentication failed!")

if __name__ == "__main__":
    main()
    