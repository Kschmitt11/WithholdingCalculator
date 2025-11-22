# user inputs filing status so we can grab the correct st deduction
# user inputs annual gross income (can expand to either monthly (can also include how many months) or annual)
# program calculates how much money will be withheld
# ADDITIONS: Deductions, tax refund calc,
TAX_BRACKETS = {
    "single": [
        (11925, 0.1),
        (48475, 0.12),
        (103350, 0.22),
        (197300, 0.24),
        (250525, 0.32),
        (626350, 0.34),
    ],
    "mfj": [
        (23850, 0.1),
        (96950, 0.12),
        (206700, 0.22),
        (394600, 0.24),
        (501050, 0.32),
        (751600, 0.34),
    ],
    "hoh": [
        (17000, 0.1),
        (64850, 0.12),
        (103350, 0.22),
        (197300, 0.24),
        (250500, 0.32),
        (626350, 0.34)
    ]
}

STANDARD_DEDUCTION = {
    "single": 15750,
    "mfj": 31500,
    "hoh": 23625
}

def get_filing_status(prompt="What is your filing status? Example: single, mfj, hoh"):
    #Asks for user's filing status to properly choose the correct tax bracket and standard deduction amount
    user_filing_status = input(prompt).lower()
    if user_filing_status.isalpha() and user_filing_status in TAX_BRACKETS.keys():
        return user_filing_status
    else:
        print("invalid input")
        return get_filing_status()



def get_gross_income(prompt="What is your gross annual income (rounded up or down)? Example: 65000"):
    #Prompts user for annual gross income and returns it for the final tax calculation
    gross_income = input(prompt).strip()
    if gross_income.isnumeric():
        return int(gross_income)

    else:
        print("invalid input")
        return get_gross_income()

def calculate_taxes(filing_status, gross_income):
    #Calculates user's taxes by using the filing status input and the user's gross income
    brackets = TAX_BRACKETS[filing_status]
    deduction = STANDARD_DEDUCTION[filing_status]
    taxable_income = gross_income - deduction

    print(taxable_income)
    taxes_owed = 0
    previous_limit = 0

    for limit, tax in brackets:
        if taxable_income > limit:
            if previous_limit == 0:
                taxes_owed += limit * tax
            else:
                taxes_owed += (limit - previous_limit) * tax
            previous_limit = limit
            # print(f"Taxes owed at {limit}: {taxes_owed}")
        else:
            taxes_owed += (taxable_income - previous_limit) * tax
            break
    print("Taxes owed:", taxes_owed)


calculate_taxes(get_filing_status(), get_gross_income())
