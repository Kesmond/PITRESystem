#app_server.py

from xmlrpc.server import SimpleXMLRPCServer
from calculator import taxableIncomeCalculator, medicalLevyCalculator, mlsCalculator, annualTaxCalculator
#from data_server import getDetailsTFN

def get_data(data): #Receives request from client application
    insurance = data[1] #True or False
    user_ID = data[2]
    biweekly_tax = data[0]
    if biweekly_tax == [(0,0)]:
        has_TFN = True
        #fetch data from database
        #If found
        #annual_taxable_income, annual_tax_witheld = annualTaxCalculator(biweekly_tax)
        #else:
            #
    else: #User doesn't have TFN
        has_TFN = False
        #Calculate the annual income and tax withheld from the biweekly pairs
        annual_taxable_income, annual_tax_witheld = annualTaxCalculator(biweekly_tax)

    #Returns back error message when encountering missing data
    if annual_taxable_income == 0:
        return "The TFN entered doesn't exist. Taxable income is not found"

    #Calculate all tax calculations
    tax = taxableIncomeCalculator(annual_taxable_income)
    ml = medicalLevyCalculator(annual_taxable_income)
    mlSurcharge = mlsCalculator(annual_taxable_income, insurance)
    total_tax = tax + ml + mlSurcharge
    net_income = annual_taxable_income - total_tax
    tax_refund_estimate = annual_tax_witheld - total_tax
    if has_TFN == True: #User does have a TFN
        returnData = [user_ID, True, annual_taxable_income, annual_tax_witheld, net_income, tax_refund_estimate, total_tax]
        #returnData = [ID, True, annual_taxable_income, annual_tax_witheld, net_income, tax_refund_estimate]
    else: #User does NOT have a TFN
        returnData = [user_ID, False, annual_taxable_income, annual_tax_witheld, net_income, tax_refund_estimate, total_tax]
    return returnData #Return data/list to client application

server = SimpleXMLRPCServer(("localhost", 8000))
print("RPC server running on port 8000...")

server.register_function(get_data, "get_data")
server.serve_forever()