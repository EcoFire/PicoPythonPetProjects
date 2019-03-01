# RentalAssessmentFunctions

# Classes and companion functions for grouping user inputs (ongoing costs, initial costs, mortgage, and tenancy

class OngoingCosts(object):
    taxes, insurance, management, capex, hoa = [0 for i in range(0, 5)]
    def __repr__(self):
        return f'OngoingCosts(taxes={self.taxes}, insurance={self.insurance}, management={self.management}, ' \
            f'capex={self.capex}, hoa={self.hoa})'

def make_OngoingCosts(Taxes_annual, Insurance_annual, Management_monthly, capex_monthly, hoa_monthly):
    OngoingCosts_ann = OngoingCosts()
    OngoingCosts_ann.taxes = Taxes_annual
    OngoingCosts_ann.insurance = Insurance_annual
    OngoingCosts_ann.management = Management_monthly * 12
    OngoingCosts_ann.capex = capex_monthly * 12
    OngoingCosts_ann.hoa = hoa_monthly * 12
    return OngoingCosts_ann


class InitialCosts(object):
    closingCosts, renovationBudget = [0 for i in range(0, 2)]
    def __repr__(self):
        return f'InitialCosts(closingCosts={self.closingCosts}, renovationBudget={self.renovationBudget})'

def make_InitialCosts(closingCosts=None, renovationBudget=None):
    costs = InitialCosts()
    InitialCost = costs
    InitialCost.closingCosts = closingCosts
    InitialCost.renovationBudget = renovationBudget
    InitialCost.total = closingCosts + renovationBudget
    return InitialCost


class Mortgage(object):
    purchaseprice, downpayment, rate, duration = [0 for i in range(0, 4)]
    def __repr__(self):
        return f'Mortgage(purchaseprice={self.purchaseprice},downpayment={self.downpayment},rate={self.rate}, duration={self.duration})'

def make_Mortgage(purchaseprice, downpayment, rate_percent, duration_years):
    mortgage = Mortgage()
    mortgage.purchaseprice = purchaseprice
    mortgage.downpayment = downpayment
    mortgage.rate = rate_percent
    mortgage.duration = duration_years
    mortgage.principal = purchaseprice - downpayment
    return mortgage


class Tenancy(object):
    rent, vacancy = [0 for i in range(0, 2)]
    def __repr__(self):
        return f'Mortgage(rent={self.rent},vacancy={self.vacancy})'

def make_Tenancy(rent_monthly, vacancy_percent):
    tenancy = Tenancy()
    tenancy.rent = rent_monthly * 12
    tenancy.vacancy = vacancy_percent
    return tenancy

#Functions to compute rental assessment and amortization table

def analyzeProperty(mortgage, tenancy, initialcosts, ongoingcosts):
    interestRate_monthly = (mortgage.rate / 100 / 12)
    PI_monthly = 12 * (interestRate_monthly * mortgage.principal) / (1 - ((1 + interestRate_monthly) ** (-30 * 12)))
    NOI_annual = tenancy.rent - ongoingcosts.management - ongoingcosts.insurance - ongoingcosts.taxes - ongoingcosts.hoa
    cashFlow_annual = NOI_annual - PI_monthly
    longTerm = tenancy.rent * 0.50 - PI_monthly - ongoingcosts.hoa
    mediumTerm = cashFlow_annual - ongoingcosts.capex - (tenancy.vacancy / 100) * tenancy.rent

    grossYield = tenancy.rent / mortgage.purchaseprice * 100
    capRate = NOI_annual / mortgage.purchaseprice * 100
    cashOnCash_perfect = cashFlow_annual / (initialcosts.total + mortgage.downpayment) * 100
    cashOnCash_average = mediumTerm / (initialcosts.total + mortgage.downpayment) * 100
    cashOnCash_poor = longTerm / (initialcosts.total + mortgage.downpayment) * 100
    return {'Gross yield': round(grossYield, 2),
            'Cap rate': round(capRate, 2),
            'Cash on Cash (perfect)': round(cashOnCash_perfect, 2),
            'Cash on Cash (average)': round(cashOnCash_average, 2),
            'Cash on Cash (bad)': round(cashOnCash_poor, 2)}

def amortizeLoan(mortgage):
    interestRate_monthly = (mortgage.rate / 100 / 12)
    PI_monthly = (interestRate_monthly * mortgage.principal) / (
                1 - ((1 + interestRate_monthly) ** (-mortgage.duration * 12)))
    remainingLoanOnPrincipal = [mortgage.principal]
    scheduleP = []
    scheduleI = []
    for i in range(0, mortgage.duration * 12):
        scheduleI.append(interestRate_monthly * remainingLoanOnPrincipal[i])
        scheduleP.append(PI_monthly - scheduleI[i])
        remainingLoanOnPrincipal.append(remainingLoanOnPrincipal[i] - scheduleP[i])
    schedule = {
        'paymentID': [i + 1 for i in range(0, mortgage.duration * 12)],
        'month': [j for i in range(0, mortgage.duration) for j in range(1, 13)],
        'year': [i + 1 for i in range(0, mortgage.duration) for j in range(1, 13)],
        'paydown': [PI_monthly * mortgage.duration * 12 - PI_monthly * i for i in range(0, mortgage.duration * 12)],
        'Equity': [int(mortgage.purchaseprice - i) for i in remainingLoanOnPrincipal],
        'Principal remaining': remainingLoanOnPrincipal}
    return {'Purchase price': mortgage.purchaseprice,
            'Down payment': mortgage.downpayment,
            'Financed': mortgage.principal,
            'Duration': mortgage.duration,
            'Payment': int(PI_monthly),
            'Total payments': int(PI_monthly * mortgage.duration * 12),
            'Schedule': schedule}




# User variables:
purchasePrice = 210000
rent_monthly = 1150

# Make inputs:
tenancy = make_Tenancy(rent_monthly=1150, vacancy_percent=5)
ongoingcosts = make_OngoingCosts(Taxes_annual=1200, Insurance_annual=500, Management_monthly=100, capex_monthly=57.50,
                                 hoa_monthly=200)
initialcosts = make_InitialCosts(closingCosts=3000, renovationBudget=0)
mortgage = make_Mortgage(purchaseprice=210000, downpayment=21000, rate_percent=4.75, duration_years=30)
