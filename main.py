# user inputs filing status so we can grab the correct st deduction
# user inputs annual gross income (can expand to either monthly (can also include how many months) or annual)
# program calculates how much money will be withheld
# ADDITIONS: Deductions, tax refund calc,
from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__) # referencing this file
CORS(app)

@app.route('/')
def index():
    return "Flask API running"


TAX_BRACKETS = {
    "single": [
        (11925, 0.1),
        (48475, 0.12),
        (103350, 0.22),
        (197300, 0.24),
        (250525, 0.32),
        (626350, 0.35),
        (math.inf, 0.37)
    ],
    "mfj": [
        (23850, 0.1),
        (96950, 0.12),
        (206700, 0.22),
        (394600, 0.24),
        (501050, 0.32),
        (751600, 0.35),
        (math.inf, 0.37)
    ],
    "hoh": [
        (17000, 0.1),
        (64850, 0.12),
        (103350, 0.22),
        (197300, 0.24),
        (250500, 0.32),
        (626350, 0.35),
        (math.inf, 0.37)
    ]
}

STANDARD_DEDUCTION = {
    "single": 15750,
    "mfj": 31500,
    "hoh": 23625
}

@app.post("/api/filing_status")
def get_filing_status():
    data = request.json
    status = data.get("status", "").lower()
    #Asks for user's filing status to properly choose the correct tax bracket and standard deduction amount
    if status in TAX_BRACKETS:
        return jsonify({"filing_status": status}), 200
    else:
        return jsonify({"error": "Invalid filing status"}), 400


@app.post("/api/gross_income")
def get_gross_income():
    #Prompts user for annual gross income and returns it for the final tax calculation
    data = request.json

    try:
        filing_status = data.get("filing_status", "").lower()
        income = float(data.get("income", 0))
    except:
        return jsonify({"error": "Invalid input types"}), 400

    if filing_status not in TAX_BRACKETS:
        return jsonify({"error": "Invalid filing status"}), 400

    if income <= 0:
        return jsonify({"error": "Income must be positive"}), 400

    taxes = calculate_taxes(filing_status, income)
    taxes = max(0, taxes)
    return jsonify({"taxes_owed": taxes}), 200


def calculate_taxes(filing_status, gross_income):
    #Calculates user's taxes by using the filing status input and the user's gross income
    brackets = TAX_BRACKETS[filing_status]
    deduction = STANDARD_DEDUCTION[filing_status]
    taxable_income = gross_income - deduction

    taxes_owed = 0
    previous_limit = 0

    for limit, tax in brackets:
        if taxable_income > limit:
            if previous_limit == 0:
                taxes_owed += limit * tax
            else:
                taxes_owed += (limit - previous_limit) * tax
                # print(f"taxes owed at {limit}: {taxes_owed}")
            previous_limit = limit

        else:
            taxes_owed += (taxable_income - previous_limit) * tax
            break

    return round(taxes_owed, 2)

if __name__ == "__main__":
    app.run(debug=True)
