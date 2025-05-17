#calculator.py

def annualTaxCalculator(biweekly_pair):
    annual_gross_income = 0
    tax_witheld = 0
    for income,tax in biweekly_pair:
        annual_gross_income += income
        tax_witheld += tax
    
    return annual_gross_income, tax_witheld

def taxableIncomeCalculator(annual_income):
    if annual_income < 18201:
        return 0
    elif annual_income < 45001:
        return 0.19*int(annual_income-18200)
    elif annual_income < 120001:
        return 5092 + (0.325*int(annual_income-45000))
    elif annual_income < 180001:
        return 29467 + (0.37*int(annual_income-120000))
    else:
        return 51667 + (45*int(annual_income-180000))
    
def medicalLevyCalculator(annual_income):
    return annual_income * 0.02
    
def mlsCalculator(annual_income, insurance):
    if insurance or annual_income < 90001:
        return 0
    elif annual_income < 105001:
        return 0.01 * annual_income
    elif annual_income < 140001:
        return 0.0125 * annual_income
    else:
        return 0.015 * annual_income