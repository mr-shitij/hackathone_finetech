"""
Helper functions for calculations and formatting
"""


def format_currency(amount: float) -> str:
    """Format amount as Indian currency"""
    return f"₹{amount:,.0f}"


def calculate_sip(monthly_amount: float, expected_return: float, time_years: int) -> dict:
    """Calculate SIP returns"""
    monthly_rate = expected_return / 100 / 12
    total_months = time_years * 12
    total_investment = monthly_amount * total_months
    
    if monthly_rate == 0:
        return {
            "total_investment": total_investment,
            "estimated_returns": 0,
            "maturity_value": total_investment
        }
    
    maturity_value = (
        monthly_amount *
        ((pow(1 + monthly_rate, total_months) - 1) / monthly_rate) *
        (1 + monthly_rate)
    )
    
    estimated_returns = maturity_value - total_investment
    
    return {
        "total_investment": round(total_investment),
        "estimated_returns": round(estimated_returns),
        "maturity_value": round(maturity_value)
    }


def calculate_emi(loan_amount: float, interest_rate: float, tenure_months: int) -> dict:
    """Calculate loan EMI"""
    monthly_rate = interest_rate / 100 / 12
    
    if monthly_rate == 0:
        emi = loan_amount / tenure_months
        return {
            "emi": round(emi),
            "total_interest": 0,
            "total_amount": round(loan_amount)
        }
    
    emi = (
        (loan_amount * monthly_rate * pow(1 + monthly_rate, tenure_months)) /
        (pow(1 + monthly_rate, tenure_months) - 1)
    )
    
    total_amount = emi * tenure_months
    total_interest = total_amount - loan_amount
    
    return {
        "emi": round(emi),
        "total_interest": round(total_interest),
        "total_amount": round(total_amount)
    }


def validate_phone_number(phone: str) -> bool:
    """Validate Indian phone number in various formats"""
    if not phone:
        return False
    
    # Remove spaces and hyphens
    phone_cleaned = phone.replace(" ", "").replace("-", "")
    
    # Check various valid formats:
    # 1. +919876543210 (E.164 format)
    # 2. 919876543210 (without +)
    # 3. 9876543210 (10 digits)
    
    if phone_cleaned.startswith("+91"):
        # +91xxxxxxxxxx format
        digits = phone_cleaned[3:]
        return len(digits) == 10 and digits.isdigit()
    elif phone_cleaned.startswith("91"):
        # 91xxxxxxxxxx format
        digits = phone_cleaned[2:]
        return len(digits) == 10 and digits.isdigit()
    else:
        # xxxxxxxxxx format (10 digits)
        return len(phone_cleaned) == 10 and phone_cleaned.isdigit()


def normalize_phone_number(phone: str) -> str:
    """
    Normalize phone number to E.164 format (+91xxxxxxxxxx)
    
    Examples:
        +919876543210 -> +919876543210
        919876543210 -> +919876543210
        9876543210 -> +919876543210
    """
    if not phone:
        return ""
    
    # Remove spaces and hyphens
    phone_cleaned = phone.replace(" ", "").replace("-", "")
    
    # Convert to E.164 format
    if phone_cleaned.startswith("+91"):
        return phone_cleaned
    elif phone_cleaned.startswith("91") and len(phone_cleaned) == 12:
        return f"+{phone_cleaned}"
    else:
        # Assume it's a 10-digit Indian number
        return f"+91{phone_cleaned}"

