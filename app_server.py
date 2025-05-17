#app_server.py

from xmlrpc.server import SimpleXMLRPCServer
from calculator import taxableIncomeCalculator, medicalLevyCalculator, mlsCalculator, annualTaxCalculator

#Data from .db
#data = {
#    "try": "Congrats!"
#}

def get_data(data):
    biweekly_tax = data[0]
    insurance = data[1]
    annual_taxable_income, annual_tax_witheld = annualTaxCalculator(biweekly_tax)

    tax = taxableIncomeCalculator(annual_taxable_income)
    ml = medicalLevyCalculator(annual_taxable_income)
    mlSurcharge = mlsCalculator(annual_taxable_income, insurance)
    total_tax = tax + ml + mlSurcharge
    net_income = annual_taxable_income - total_tax
    tax_refund_estimate = annual_tax_witheld - total_tax
    #returnData = [ID, "NO TFN", annual_taxable_income, annual_tax_witheld, net_income, tax_refund_estimate]
    returnData = [annual_taxable_income, annual_tax_witheld, net_income, tax_refund_estimate, total_tax]
    return returnData

server = SimpleXMLRPCServer(("localhost", 8000))
print("RPC server running on port 8000...")

server.register_function(get_data, "get_data")
server.serve_forever()