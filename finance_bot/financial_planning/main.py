import os
import json
import yaml
from crewai import Agent, Task, Crew, Process
from langchain.llms import Ollama
from finance_bot.financial_planning.tools.custom_tool import SearchTool

# Define file paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(CURRENT_DIR, 'config')
AGENTS_CONFIG = os.path.join(CONFIG_DIR, 'agents.yaml')
TASKS_CONFIG = os.path.join(CONFIG_DIR, 'tasks.yaml')

def load_config(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

class FinancialPlanningCrew:
    def __init__(self, user_data_json):
        self.user_data = self._enrich_user_data(user_data_json)
        self.agents_config = load_config(AGENTS_CONFIG)
        self.tasks_config = load_config(TASKS_CONFIG)
        self.search_tool = SearchTool()
        
        # Initialize Ollama LLM using LangChain
        self.llm = Ollama(
            model="mistral-nemo",
            base_url="http://localhost:11434"
        )

    def _enrich_user_data(self, user_data):
        """Perform deterministic calculations and inject into user_data"""
        # Calculate Total Assets
        assets = user_data['financials'].get('assets', {})
        total_assets = sum(assets.values()) if assets else 0
        
        # Calculate Total Liabilities
        liabilities = user_data['financials'].get('liabilities', {})
        total_liabilities = sum(liabilities.values()) if liabilities else 0
        
        # Calculate Net Worth (can be negative!)
        net_worth = total_assets - total_liabilities
        
        # Calculate Monthly Cash Flow
        income = user_data['financials'].get('income', {})
        expenses = user_data['financials'].get('expenses', {})
        monthly_income = income.get('monthly_salary', 0)
        monthly_expenses = expenses.get('monthly_fixed', 0) + expenses.get('monthly_variable', 0)
        monthly_surplus = monthly_income - monthly_expenses
        
        # Annual figures
        annual_bonus = income.get('annual_bonus', 0)
        total_annual_income = (monthly_income * 12) + annual_bonus
        
        # Savings rate
        if total_annual_income > 0:
            annual_savings = (monthly_surplus * 12)
            savings_rate = (annual_savings / total_annual_income) * 100
        else:
            savings_rate = 0
        
        # Inject pre-calculated values
        if 'pre_calculated_metrics' not in user_data:
            user_data['pre_calculated_metrics'] = {}
            
        user_data['pre_calculated_metrics'].update({
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'net_worth': net_worth,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'monthly_surplus': monthly_surplus,
            'total_annual_income': total_annual_income,
            'savings_rate': round(savings_rate, 2),
            'has_negative_cash_flow': monthly_surplus < 0,
            'is_overleveraged': total_liabilities > (total_annual_income * 5) if total_annual_income > 0 else False
        })
        
        if monthly_surplus < 0:
            user_data['pre_calculated_metrics']['critical_warning'] = f"User has negative cash flow of ₹{abs(monthly_surplus):,}/month. URGENT expense reduction or income increase required."
            
        return user_data

    def create_agents(self):
        self.financial_analyst = Agent(
            role=self.agents_config['financial_analyst']['role'],
            goal=self.agents_config['financial_analyst']['goal'],
            backstory=self.agents_config['financial_analyst']['backstory'],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

        self.research_specialist = Agent(
            role=self.agents_config['research_specialist']['role'],
            goal=self.agents_config['research_specialist']['goal'],
            backstory=self.agents_config['research_specialist']['backstory'],
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool],
            llm=self.llm
        )

        self.strategy_advisor = Agent(
            role=self.agents_config['strategy_advisor']['role'],
            goal=self.agents_config['strategy_advisor']['goal'],
            backstory=self.agents_config['strategy_advisor']['backstory'],
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )

        self.report_generator = Agent(
            role=self.agents_config['report_generator']['role'],
            goal=self.agents_config['report_generator']['goal'],
            backstory=self.agents_config['report_generator']['backstory'],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def create_tasks(self):
        # Pass user_data as a string to the task description
        user_data_str = json.dumps(self.user_data, indent=2)

        self.analysis_task = Task(
            description=self.tasks_config['analysis_task']['description'].format(user_data=user_data_str),
            expected_output=self.tasks_config['analysis_task']['expected_output'],
            agent=self.financial_analyst
        )

        self.research_task = Task(
            description=self.tasks_config['research_task']['description'].format(user_data=user_data_str),
            expected_output=self.tasks_config['research_task']['expected_output'],
            agent=self.research_specialist
        )

        self.strategy_task = Task(
            description=self.tasks_config['strategy_task']['description'],
            expected_output=self.tasks_config['strategy_task']['expected_output'],
            agent=self.strategy_advisor,
            context=[self.analysis_task, self.research_task] # Depends on analysis and research
        )

        self.report_task = Task(
            description=self.tasks_config['report_task']['description'].format(user_data=user_data_str),
            expected_output=self.tasks_config['report_task']['expected_output'],
            agent=self.report_generator,
            context=[self.analysis_task, self.research_task, self.strategy_task]
        )

    def run(self):
        self.create_agents()
        self.create_tasks()

        crew = Crew(
            agents=[
                self.financial_analyst,
                self.research_specialist,
                self.strategy_advisor,
                self.report_generator
            ],
            tasks=[
                self.analysis_task,
                self.research_task,
                self.strategy_task,
                self.report_task
            ],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        return result

if __name__ == "__main__":
    # Load sample user data
    user_data_path = os.path.join(CURRENT_DIR, 'user_data.json')
    with open(user_data_path, 'r') as f:
        user_data = json.load(f)

    print("Starting Financial Planning Crew...")
    
    # PRE-CALCULATION STEP (Deterministic)
    # Calculate key metrics to ensure 100% accuracy
    print("Performing deterministic financial calculations...")
    
    # Calculate Total Assets
    assets = user_data['financials']['assets']
    total_assets = sum(assets.values())
    
    # Calculate Total Liabilities
    liabilities = user_data['financials'].get('liabilities', {})
    total_liabilities = sum(liabilities.values())
    
    # Calculate Net Worth (can be negative!)
    net_worth = total_assets - total_liabilities
    
    # Calculate Monthly Cash Flow
    income = user_data['financials']['income']
    expenses = user_data['financials']['expenses']
    monthly_income = income.get('monthly_salary', 0)
    monthly_expenses = expenses.get('monthly_fixed', 0) + expenses.get('monthly_variable', 0)
    monthly_surplus = monthly_income - monthly_expenses
    
    # Annual figures
    annual_bonus = income.get('annual_bonus', 0)
    total_annual_income = (monthly_income * 12) + annual_bonus
    
    # Savings rate
    if total_annual_income > 0:
        annual_savings = (monthly_surplus * 12)
        savings_rate = (annual_savings / total_annual_income) * 100
    else:
        savings_rate = 0
    
    # Inject pre-calculated values
    user_data['pre_calculated_metrics'] = {
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'net_worth': net_worth,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'monthly_surplus': monthly_surplus,
        'total_annual_income': total_annual_income,
        'savings_rate': round(savings_rate, 2),
        'has_negative_cash_flow': monthly_surplus < 0,
        'is_overleveraged': total_liabilities > (total_annual_income * 5) if total_annual_income > 0 else False
    }
    
    print(f"  Net Worth: ₹{net_worth:,}")
    print(f"  Monthly Cash Flow: ₹{monthly_surplus:,}")
    print(f"  Savings Rate: {savings_rate:.1f}%")
    
    if monthly_surplus < 0:
        print(f"  ⚠️  WARNING: NEGATIVE CASH FLOW DETECTED!")
        user_data['pre_calculated_metrics']['critical_warning'] = f"User has negative cash flow of ₹{abs(monthly_surplus):,}/month. URGENT expense reduction or income increase required."
    
    print("Pre-calculation completed.\n")
    
    finance_crew = FinancialPlanningCrew(user_data)
    result = finance_crew.run()
    
    print("\n\n########################")
    print("## FINAL FINANCIAL PLAN ##")
    print("########################\n")
    print(result)
    
    # Save output to file
    output_path = os.path.join(CURRENT_DIR, 'financial_plan_report.md')
    with open(output_path, 'w') as f:
        f.write(str(result))
    print(f"\nReport saved to: {output_path}")

