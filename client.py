#client.py
import xmlrpc.client

def biweeklyIncomeCalculator():
    print("Enter up to 26 biweekly income and tax withheld (e.g. 'income tax')")
    tax_pairs = []
    sum_income = 0
    sum_tax = 0
    week = 1
    while week <= 26:
        weekly_pair = input(f"Enter biweekly income (Week {week}) or 'done' to finish: ")

        if weekly_pair.lower() == 'done':
            print("Exited by user.")
            break

        try:
            income, tax = map(float, weekly_pair.split())
            sum_income = sum_income + income
            sum_tax = sum_tax + tax
            tax_pairs.append((income,tax))
            week += 1
        except ValueError:
            print("Invalid input. Please enter two numbers, separated by space.")

    return sum_income, sum_tax


def main():
    #Authentication
    #ID 6 digit and password
    #uri = input("Authentication/Enter the server URI: ")
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    #Implementation
    income_pairs = 0
    print("Welcome User!")
    print("Please enter your 8 digit TFN number! (-1 if you don't have)")
    tfn = int(input("Enter your Tax File Number (TFN): "))
    print(tfn)
    if tfn == -1:
        print("Authentication Failed!\n")
        income_pairs = biweeklyIncomeCalculator()
    #print(income_pairs)
    
    have_PHIC = input("\nDo you have a Private Health Insurance Cover? (y/n): ").lower() == 'y'

    data = [income_pairs, have_PHIC]
    try:
        result = proxy.get_data(data)

        if type(result) is str:
            print()
        else:
            print("")
            #print(ID)
            print("NO TFN")
            print(f"Annual Taxable Income: ", result[0])
            print(f"Total Tax Witheld: ", result[1])
            print(f"Total net-income: ", result[2])
            print(f"Estimated tax refund amount: ", result[3])
    except Exception as e:
        print("Error {e}")

if __name__ == "__main__":
    main()

#Eligible TFN then print user information

#Otherwise
#Request for ID, biweekly (taxable_income, tax_witheld) pair
#Health Insurance

#Print Tax Return Estimate Result