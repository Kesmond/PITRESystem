#app_server.py
import requests

from xmlrpc.server import SimpleXMLRPCServer
from calculator import taxableIncomeCalculator, medicalLevyCalculator, mlsCalculator, annualTaxCalculator

DATA_SERVER_URL = "http://localhost:5001/get_record"

class TaxService:
    def get_record(self, tfn):
        #Function to get data from data server
        try:
            #Request data from data_server by passing TFN value, and stores the result to "response" variable
            response = requests.get(DATA_SERVER_URL, params={"tfn": tfn})
            if response.status_code == 200: #If succeed
                data = response.json() #Store to "data" variable and return
                return [
                    data.get("tfn"),
                    data.get("biweekly_tax_pairs"),
                    data.get("fname"),
                    data.get("lname"),
                    data.get("email"),
                    data.get("id")
                ]
            else: #If any error occured
                return f"Error: {response.status_code}"
        except requests.ConnectionError: #Database server offline
            return "Server Error: Cannot connect to server 2 or database server"

    def get_data(self, data): #Receives request from client application
        biweekly_tax = data['income_pairs']
        insurance = data['insurance'] #True or False
        user_ID = data['user_id']
        tfn = data['tfn']
        user_info = data.get('user_information', {})
        
        #If the tax pair is (0,0) [TAXPAYER HAS TFN]
        if biweekly_tax == [[0,0]]:
            #Fetches the tax pair from get_record function, passing TFN as parameter
            database_information = self.get_record(tfn)
            #If the value returned from the function is a string (error message)
            if type(database_information) is str:
                return database_information #Return the error message
            if not database_information: #If there's nothing
                return "TFN not found in database" #TFN is not found in the database
                        
            #Store the values received from the database for proper naming
            tfn, biweekly_tax, fname, lname, email, id = database_information
            #Rename the data entered by user for proper naming
            fname_entered = user_info['f_name']
            lname_entered = user_info['l_name']
            email_entered = user_info['email']
            
            #If the user ID used to login doesn't match with TFN's id the database
            if int(user_ID) != int(id): #A user CANNOT access other's records
                return "You can't access others TFN!"
            #Second level authentication, credentials entered matches the TFN's id in the database
            elif fname_entered != fname or lname_entered != lname or email_entered != email:
                return "Personal information doesn't match"
            has_TFN = True #Valid TFN
        else: #User doesn't have TFN
            has_TFN = False

        #Calculate the annual income and tax withheld from the biweekly pairs
        annual_taxable_income, annual_tax_witheld = annualTaxCalculator(biweekly_tax)

        #Returns back error message when encountering income = 0
        if annual_taxable_income == 0:
            return "No income this year."

        #Calculate all tax calculations
        tax = taxableIncomeCalculator(annual_taxable_income)
        ml = medicalLevyCalculator(annual_taxable_income)
        mlSurcharge = mlsCalculator(annual_taxable_income, insurance)
        total_tax = tax + ml + mlSurcharge
        net_income = annual_taxable_income - total_tax
        tax_refund_estimate = annual_tax_witheld - total_tax

        #Returns all the calculated value to client application
        if has_TFN == True: #User does have a TFN
            returnData = [user_ID, True, annual_taxable_income, annual_tax_witheld, net_income, tax_refund_estimate, total_tax]
        else: #User does NOT have a TFN
            returnData = [user_ID, False, annual_taxable_income, annual_tax_witheld, net_income, tax_refund_estimate, total_tax]
        return returnData #Return data/list to client application

server = SimpleXMLRPCServer(("localhost", 8000))
print("RPC server running on port 8000...")

server.register_instance(TaxService())
server.serve_forever()