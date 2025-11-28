import os
import json
import yaml
from crewai import Agent, Task, Crew, Process, LLM
from finance_bot.tax_planning.tools.tax_calculator import TaxCalculatorTool

# Import search tool from financial planning
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'financial_planning'))
from tools.custom_tool import SearchTool

# Define file paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(CURRENT_DIR, 'config')
AGENTS_CONFIG = os.path.join(CONFIG_DIR, 'agents.yaml')
TASKS_CONFIG = os.path.join(CONFIG_DIR, 'tasks.yaml')

def load_config(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

class TaxPlanningCrew:
    def __init__(self, user_data_json):
        self.user_data = user_data_json
        self.agents_config = load_config(AGENTS_CONFIG)
        self.tasks_config = load_config(TASKS_CONFIG)
        
        # Initialize tools
        self.tax_calculator_tool = TaxCalculatorTool()
        self.search_tool = SearchTool()
        
        # Initialize Ollama LLM using CrewAI's native LLM class
        self.llm = LLM(
            model="ollama/mistral-nemo",
            base_url="http://localhost:11434"
        )

    def create_agents(self):
        self.tax_calculator = Agent(
            role=self.agents_config['tax_calculator']['role'],
            goal=self.agents_config['tax_calculator']['goal'],
            backstory=self.agents_config['tax_calculator']['backstory'],
            verbose=True,
            allow_delegation=False,
            tools=[self.tax_calculator_tool],
            llm=self.llm
        )

        self.deduction_analyzer = Agent(
            role=self.agents_config['deduction_analyzer']['role'],
            goal=self.agents_config['deduction_analyzer']['goal'],
            backstory=self.agents_config['deduction_analyzer']['backstory'],
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
        user_data_str = json.dumps(self.user_data, indent=2)

        self.tax_calculation_task = Task(
            description=self.tasks_config['tax_calculation_task']['description'].format(user_data=user_data_str),
            expected_output=self.tasks_config['tax_calculation_task']['expected_output'],
            agent=self.tax_calculator
        )

        self.deduction_analysis_task = Task(
            description=self.tasks_config['deduction_analysis_task']['description'].format(user_data=user_data_str),
            expected_output=self.tasks_config['deduction_analysis_task']['expected_output'],
            agent=self.deduction_analyzer,
            context=[self.tax_calculation_task]
        )

        self.strategy_task = Task(
            description=self.tasks_config['strategy_task']['description'],
            expected_output=self.tasks_config['strategy_task']['expected_output'],
            agent=self.strategy_advisor,
            context=[self.tax_calculation_task, self.deduction_analysis_task]
        )

        self.report_task = Task(
            description=self.tasks_config['report_task']['description'].format(user_data=user_data_str),
            expected_output=self.tasks_config['report_task']['expected_output'],
            agent=self.report_generator,
            context=[self.tax_calculation_task, self.deduction_analysis_task, self.strategy_task]
        )

    def run(self):
        self.create_agents()
        self.create_tasks()

        crew = Crew(
            agents=[
                self.tax_calculator,
                self.deduction_analyzer,
                self.strategy_advisor,
                self.report_generator
            ],
            tasks=[
                self.tax_calculation_task,
                self.deduction_analysis_task,
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
    user_data_path = os.path.join(CURRENT_DIR, 'user_tax_data.json')
    with open(user_data_path, 'r') as f:
        user_data = json.load(f)

    print("Starting Tax Planning Crew...")
    
    # PRE-CALCULATION STEP (Deterministic)
    # We calculate tax here to ensure 100% accuracy and avoid LLM tool-calling errors
    print("Performing deterministic tax calculation...")
    calculator = TaxCalculatorTool()
    
    # Calculate Gross Income
    salary = user_data['income']['salary']
    other = user_data['income']['other_income']
    gross_salary = salary['basic_salary'] + salary['hra'] + salary['allowances'] + salary['bonus']
    gross_other = other['interest_savings'] + other['interest_fd'] + other['dividend']
    gross_total = gross_salary + gross_other
    
    # Calculate Deductions
    sec_80c = sum(user_data['current_investments']['section_80c'].values())
    sec_80d = sum(user_data['current_investments']['section_80d'].values())
    
    # Run Calculator
    old_regime_tax = calculator._run(income=gross_total, deductions_80c=sec_80c, deductions_80d=sec_80d, regime="old")
    new_regime_tax = calculator._run(income=gross_total, regime="new")
    
    # Inject results into user_data
    user_data['tax_calculation_results'] = {
        'gross_income': gross_total,
        'deductions_80c': sec_80c,
        'deductions_80d': sec_80d,
        'old_regime_report': old_regime_tax,
        'new_regime_report': new_regime_tax
    }
    
    print("Tax calculation completed and injected into context.")
    
    tax_crew = TaxPlanningCrew(user_data)
    result = tax_crew.run()
    
    print("\n\n########################")
    print("## TAX PLANNING REPORT ##")
    print("########################\n")
    print(result)
    
    # Save output to file
    output_path = os.path.join(CURRENT_DIR, 'tax_planning_report.md')
    with open(output_path, 'w') as f:
        f.write(str(result))
    print(f"\nReport saved to: {output_path}")
