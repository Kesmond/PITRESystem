#app_server.py

from xmlrpc.server import SimpleXMLRPCServer
from calculator import taxableIncomeCalculator, medicalLevyCalculator, mlsCalculator, annualTaxCalculator

#Data from .db
#data = {
#    "try": "Congrats!"
#}

def get_data(data):
    insurance = data[1] #True or False
    user_ID = data[2]
    if biweekly_tax == [(0,0)]:
        has_TFN = True
        #fetch data from database
        #If found
        #annual_taxable_income, annual_tax_witheld = annualTaxCalculator(biweekly_tax)
        #else:
            #
    else:
        has_TFN = False
        biweekly_tax = data[0]
        annual_taxable_income, annual_tax_witheld = annualTaxCalculator(biweekly_tax)

    #Returns back error message when encountering missing data
    if annual_tax_witheld == 0:
        return "The TFN entered doesn't exist."
    elif annual_taxable_income == 0:
        return "The TFN entered doesn't exist. Taxable income is not found"

    tax = taxableIncomeCalculator(annual_taxable_income)
    ml = medicalLevyCalculator(annual_taxable_income)
    mlSurcharge = mlsCalculator(annual_taxable_income, insurance)
    total_tax = tax + ml + mlSurcharge
    net_income = annual_taxable_income - total_tax
    tax_refund_estimate = annual_tax_witheld - total_tax
    if has_TFN == True:
        returnData = [user_ID, True, annual_taxable_income, annual_tax_witheld, net_income, tax_refund_estimate, total_tax]
        #returnData = [ID, True, annual_taxable_income, annual_tax_witheld, net_income, tax_refund_estimate]
    else: 
        returnData = [user_ID, False, annual_taxable_income, annual_tax_witheld, net_income, tax_refund_estimate, total_tax]
    return returnData

server = SimpleXMLRPCServer(("localhost", 8000))
print("RPC server running on port 8000...")

server.register_function(get_data, "get_data")
server.serve_forever()