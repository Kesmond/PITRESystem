#app_server.py
import requests

from xmlrpc.server import SimpleXMLRPCServer
from calculator import taxableIncomeCalculator, medicalLevyCalculator, mlsCalculator, annualTaxCalculator

DATA_SERVER_URL = "http://localhost:5001/get_record"

class TaxService:
    def get_record(self, tfn):
        #Gets data from data server
        try:
            response = requests.get(DATA_SERVER_URL, params={"tfn": tfn})
            if response.status_code == 200:
                data = response.json()
                return [
                    data.get("tfn"),
                    data.get("biweekly_tax_pairs"),
                    data.get("fname"),
                    data.get("lname"),
                    data.get("email")
                ]
            else:
                return f"Error: {response.status_code}"
        except requests.ConnectionError:
            return "Server Error: Cannot connect to server 2 or database server"

    def get_data(self, data): #Receives request from client application
        biweekly_tax = data['income_pairs']
        insurance = data['insurance'] #True or False
        user_ID = data['user_id']
        tfn = data['tfn']
        user_info = data.get('user_information', {})
        
        if biweekly_tax == [[0,0]]:
            database_information = self.get_record(tfn)
            if type(database_information) is str:
                return database_information
            if not database_information:
                return "TFN not found in database"
                        
            tfn, biweekly_tax, fname, lname, email = database_information
            fname_entered = user_info['f_name']
            lname_entered = user_info['l_name']
            email_entered = user_info['email']
            
            #Check if user_information (fname,lname,email) matches in the database
            if fname_entered != fname or lname_entered != lname or email_entered != email:
                return "Personal information doesn't match"
            has_TFN = True
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
        if has_TFN == True: #User does have a TFN
            returnData = [user_ID, True, annual_taxable_income, annual_tax_witheld, net_income, tax_refund_estimate, total_tax]
        else: #User does NOT have a TFN
            returnData = [user_ID, False, annual_taxable_income, annual_tax_witheld, net_income, tax_refund_estimate, total_tax]
        return returnData #Return data/list to client application

server = SimpleXMLRPCServer(("localhost", 8000))
print("RPC server running on port 8000...")

server.register_instance(TaxService())
server.serve_forever()