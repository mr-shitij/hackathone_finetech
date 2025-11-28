from crewai.tools import BaseTool

class TaxCalculatorTool(BaseTool):
    name: str = "TaxCalculator"
    description: str = "Calculates Indian income tax liability based on income and deductions for both old and new tax regimes."

    def _run(self, income: float, deductions_80c: float = 0, deductions_80d: float = 0, 
             deductions_other: float = 0, regime: str = "old") -> str:
        """
        Calculate tax liability for Indian taxpayers.
        
        Args:
            income: Gross total income in INR
            deductions_80c: Section 80C deductions (max 150000)
            deductions_80d: Section 80D deductions (max 50000)
            deductions_other: Other deductions
            regime: "old" or "new"
        
        Returns:
            Tax calculation breakdown
        """
        
        if regime == "new":
            # New regime tax slabs for FY 2024-25
            standard_deduction = 75000
            taxable_income = max(0, income - standard_deduction)
            
            # New regime slabs
            if taxable_income <= 300000:
                tax = 0
            elif taxable_income <= 700000:
                tax = (taxable_income - 300000) * 0.05
            elif taxable_income <= 1000000:
                tax = 20000 + (taxable_income - 700000) * 0.10
            elif taxable_income <= 1200000:
                tax = 50000 + (taxable_income - 1000000) * 0.15
            elif taxable_income <= 1500000:
                tax = 80000 + (taxable_income - 1200000) * 0.20
            else:
                tax = 140000 + (taxable_income - 1500000) * 0.30
            
            # Tax rebate for income up to 7 lakh
            if taxable_income <= 700000:
                tax = max(0, tax - 25000)
            
            cess = tax * 0.04
            total_tax = tax + cess
            
            return f"""New Regime Tax Calculation:
Gross Income: ₹{income:,.0f}
Standard Deduction: ₹{standard_deduction:,.0f}
Taxable Income: ₹{taxable_income:,.0f}
Income Tax: ₹{tax:,.0f}
Health & Education Cess (4%): ₹{cess:,.0f}
Total Tax Liability: ₹{total_tax:,.0f}
"""
        
        else:  # Old regime
            # Apply deductions
            total_deductions = min(deductions_80c, 150000) + min(deductions_80d, 50000) + deductions_other
            taxable_income = max(0, income - total_deductions)
            
            # Old regime slabs
            if taxable_income <= 250000:
                tax = 0
            elif taxable_income <= 500000:
                tax = (taxable_income - 250000) * 0.05
            elif taxable_income <= 1000000:
                tax = 12500 + (taxable_income - 500000) * 0.20
            else:
                tax = 112500 + (taxable_income - 1000000) * 0.30
            
            # Tax rebate under section 87A
            if taxable_income <= 500000:
                tax = max(0, tax - 12500)
            
            cess = tax * 0.04
            total_tax = tax + cess
            
            return f"""Old Regime Tax Calculation:
Gross Income: ₹{income:,.0f}
80C Deductions: ₹{min(deductions_80c, 150000):,.0f}
80D Deductions: ₹{min(deductions_80d, 50000):,.0f}
Other Deductions: ₹{deductions_other:,.0f}
Total Deductions: ₹{total_deductions:,.0f}
Taxable Income: ₹{taxable_income:,.0f}
Income Tax: ₹{tax:,.0f}
Health & Education Cess (4%): ₹{cess:,.0f}
Total Tax Liability: ₹{total_tax:,.0f}
"""
