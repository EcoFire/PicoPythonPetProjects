'''
Justin Ziegler
3/1/2019
Rental Assessment Example
This program analyzes the financial returns on investment for a rental property
The functions are strictly focused on cash flow and don't account for appreciation or depreciation of a rental unit,
in other words these are the financial consequences of a buy-and-hold strategy
One important assumption is that there is no private mortgage insurance
'''
from RentalCashFlowAnalysis import RentalAssessment

# Make inputs:
tenancy = RentalAssessment.make_Tenancy(rent_monthly=1500, vacancy_percent=2)
ongoingcosts = RentalAssessment.make_OngoingCosts(Taxes_annual=1200, Insurance_annual=500, Management_monthly=100,
                                                  capex_monthly=57.50, hoa_monthly=200)
initialcosts = RentalAssessment.make_InitialCosts(closingCosts=3000, renovationBudget=0)
mortgage = RentalAssessment.make_Mortgage(purchaseprice=210000, downpayment=42000, rate_percent=4.75, duration_years=30)

# Anaylze property
RentalAssessment.analyzeProperty(mortgage=mortgage, tenancy=tenancy,
                                 initialcosts=initialcosts,ongoingcosts=ongoingcosts)
# Some definitions are required:
# Gross yield is the return on investment prior to any costs or deductions. It is simply, the annual revenue
# of an investment as a percent of the purchase price
# Cap rate is the yield as a percent of the purchase price net of ongoing costs of taxes, insurance,
# HOA fees, and property management. This is the equivalent of buying a property in full with cash
# Cash on cash (perfect) is the yield as a percent of cash outlay net of ongoing and financing costs.
# It does not deduct vacancy or capital expenditures.
# Cash on cash (average) is similar to cash on cash (perfect) net of vacancy and captial expenditures.
# Cash on cash (bad) is similar to cash on cash (perfect) net of vacancy where vacancy is 50% (i.e. the investment is
# vacant for half the year.

#Produce amortization table
amortization = RentalAssessment.amortizeLoan(mortgage=mortgage)
amortization.keys()
amortization.values()
amortization['Schedule'].keys()
# This function creates an amortization table. It holds the basic information: purchase price, down payment, amount
# financed, the duration of the loan, the monthly payment amount, and the total payments over the duration of the loan
# It also holds, within Schedule, a dictionary with each payment's occurrence by month and year and containing:
# how much total principal and interest remains, accrued equity, and how much principal remains.
