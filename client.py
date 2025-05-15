#client.py
import xmlrpc.client

#ID 6 digit and password
#uri = input("Authentication/Enter the server URI: ")
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

#Implementation
print("Welcome User!")
print("Please enter your TFN! (-1 if you don't have)")
tfn = input("Enter your TFN: ")
result = proxy.get_data(tfn)
print(result)

#Eligible TFN then print user information

#Otherwise
#Request for ID, biweekly (taxable_income, tax_witheld) pair
#Health Insurance

#Print Tax Return Estimate Result