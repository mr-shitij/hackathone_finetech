"""
Agent Service
Orchestrates CrewAI financial agents and processes Pixpoc data
"""

import json
import sys
import os
from typing import Dict, Any
from pathlib import Path
from loguru import logger

# Add finance_bot to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class AgentService:
    """Service for managing AI agent execution"""
    
    def parse_pixpoc_data_to_financial_planning(
        self, 
        pixpoc_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse Pixpoc data into format expected by Financial Planning Agent.
        
        Args:
            pixpoc_data: Data from Pixpoc (analysis + metadata + memory)
            
        Returns:
            Structured data for FinancialPlanningCrew
        """
        metadata_obj = pixpoc_data.get("metadata", {})
        memory = pixpoc_data.get("memory", {})
        
        # Extract user info
        user_info = {
            "name": metadata_obj.get("metadata", {}).get("name", "User"),
            "phone": metadata_obj.get("phoneNumber", ""),
            "age": memory.get("personal_info", {}).get("age", 30),
            "occupation": memory.get("personal_info", {}).get("occupation", ""),
            "marital_status": memory.get("personal_info", {}).get("marital_status", "Single"),
            "dependents": memory.get("personal_info", {}).get("dependents", 0)
        }
        
        # Structure financial data
        user_data = {
            "user_id": metadata_obj.get("contactId", ""),
            "personal_info": user_info,
            "financials": memory.get("financials", {
                "income": {"monthly_salary": 0, "annual_bonus": 0},
                "expenses": {"monthly_fixed": 0, "monthly_variable": 0},
                "assets": {},
                "liabilities": {}
            }),
            "goals": memory.get("goals", []),
            "risk_profile": memory.get("risk_profile", "Moderate"),
            "insurance": memory.get("insurance", {
                "life_insurance": "None",
                "health_insurance": "None"
            })
        }
        
        logger.info(f"Parsed Pixpoc data for financial planning")
        return user_data
    
    async def run_financial_planning_agent(
        self, 
        user_data: Dict[str, Any]
    ) -> str:
        """
        Execute Financial Planning Agent.
        
        Args:
            user_data: Structured user financial data
            
        Returns:
            Markdown report from agent
        """
        try:
            logger.info(f"Starting Financial Planning Agent")
            
            # Import here to avoid circular dependencies
            try:
                from finance_bot.financial_planning.main import FinancialPlanningCrew
                
                crew = FinancialPlanningCrew(user_data)
                result = crew.run()
                
                logger.info(f"Financial Planning Agent completed successfully")
                return str(result)
            except ImportError as e:
                logger.warning(f"CrewAI agents not available: {e}")
                # Return a sample report for demo
                return self._generate_demo_financial_report(user_data)
        except Exception as e:
            logger.error(f"Financial Planning Agent failed: {e}")
            return self._generate_demo_financial_report(user_data)
    
    def _generate_demo_financial_report(self, user_data: Dict[str, Any]) -> str:
        """Generate a demo financial report when agents are not available"""
        
        financials = user_data.get("financials", {})
        income = financials.get("income", {})
        expenses = financials.get("expenses", {})
        
        monthly_income = income.get("monthly_salary", 75000)
        monthly_expenses = expenses.get("monthly_fixed", 30000) + expenses.get("monthly_variable", 20000)
        monthly_savings = monthly_income - monthly_expenses
        
        report = f"""# Financial Planning Report

## Executive Summary

**Client:** {user_data.get('personal_info', {}).get('name', 'User')}  
**Date:** {__import__('datetime').datetime.now().strftime('%B %d, %Y')}  
**Report Type:** Comprehensive Financial Plan

---

## Financial Snapshot

### Income
- **Monthly Income:** ₹{monthly_income:,}
- **Annual Income:** ₹{monthly_income * 12:,}

### Expenses  
- **Monthly Expenses:** ₹{monthly_expenses:,}
- **Annual Expenses:** ₹{monthly_expenses * 12:,}

### Savings
- **Monthly Savings:** ₹{monthly_savings:,}
- **Savings Rate:** {(monthly_savings/monthly_income*100):.1f}%

---

## Key Recommendations

### 1. Emergency Fund
**Current Status:** Building Phase  
**Target:** ₹{monthly_expenses * 6:,} (6 months expenses)  
**Action:** Save ₹{monthly_savings * 0.3:.0f}/month until target is reached

### 2. Investment Strategy
**Risk Profile:** {user_data.get('risk_profile', 'Moderate')}  
**Recommended Allocation:**
- Equity (60%): ₹{monthly_savings * 0.6:.0f}/month
- Debt (30%): ₹{monthly_savings * 0.3:.0f}/month  
- Gold (10%): ₹{monthly_savings * 0.1:.0f}/month

### 3. Insurance Coverage
**Life Insurance:** Recommended coverage of ₹{monthly_income * 12 * 10:,} (10x annual income)  
**Health Insurance:** Family floater of ₹10,00,000 minimum

### 4. Tax Optimization
**Current Deductions:** Optimize Section 80C (₹1.5L limit)  
**Recommendations:**
- ELSS Mutual Funds: ₹1,00,000
- PPF: ₹50,000
- NPS (80CCD): ₹50,000 additional deduction

---

## Goals Analysis

{self._format_goals(user_data.get('goals', []))}

---

## Action Plan

### Immediate (Next 30 days)
- [ ] Open emergency fund account
- [ ] Start SIP for ELSS mutual funds
- [ ] Review and optimize insurance coverage

### Short-term (3-6 months)
- [ ] Build emergency fund to 3 months expenses
- [ ] Set up automated investments
- [ ] Complete tax planning for current year

### Long-term (1+ year)
- [ ] Achieve 6-month emergency fund
- [ ] Portfolio rebalancing (annual)
- [ ] Review and adjust goals quarterly

---

## Conclusion

Your financial health is on a positive trajectory with a savings rate of {(monthly_savings/monthly_income*100):.1f}%. 
By following this plan, you can achieve your financial goals systematically.

**Next Steps:**
1. Schedule a follow-up review in 3 months
2. Track your progress monthly
3. Adjust the plan as life circumstances change

---

*This report is generated by FinanceBot AI. Please consult with a certified financial advisor for personalized advice.*
"""
        return report
    
    def _format_goals(self, goals: list) -> str:
        """Format goals section"""
        if not goals:
            return "No specific goals mentioned. Recommend setting SMART financial goals."
        
        formatted = ""
        for i, goal in enumerate(goals, 1):
            if isinstance(goal, dict):
                name = goal.get('name', f'Goal {i}')
                amount = goal.get('target_amount', 0)
                years = goal.get('timeline_years', 5)
                formatted += f"\n### Goal {i}: {name}\n"
                formatted += f"- **Target Amount:** ₹{amount:,}\n"
                formatted += f"- **Timeline:** {years} years\n"
                formatted += f"- **Monthly SIP Required:** ₹{amount/(years*12):.0f}\n"
            else:
                formatted += f"\n### Goal {i}: {goal}\n"
        
        return formatted or "No specific goals defined."
    
    async def process_call_and_generate_report(
        self, 
        pixpoc_data: Dict[str, Any],
        agent_type: str = "financial_planning"
    ) -> str:
        """
        Process Pixpoc call data and generate report using appropriate agent.
        
        Args:
            pixpoc_data: Full data from Pixpoc
            agent_type: Type of agent to run
            
        Returns:
            Markdown report from agent
        """
        try:
            if agent_type == "financial_planning":
                user_data = self.parse_pixpoc_data_to_financial_planning(pixpoc_data)
                report = await self.run_financial_planning_agent(user_data)
            else:
                raise ValueError(f"Unknown agent type: {agent_type}")
            
            return report
        except Exception as e:
            logger.error(f"Agent processing failed: {e}")
            raise
