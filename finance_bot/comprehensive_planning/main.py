import os
import json
import yaml
from crewai import Agent, Task, Crew, Process, LLM
from finance_bot.financial_planning.tools.custom_tool import search_tool
from finance_bot.tax_planning.tools.tax_calculator import tax_calculator_tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define file paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(CURRENT_DIR, 'config')
AGENTS_CONFIG = os.path.join(CONFIG_DIR, 'agents.yaml')
TASKS_CONFIG = os.path.join(CONFIG_DIR, 'tasks.yaml')

def load_config(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

class ComprehensivePlanningCrew:
    """
    Unified crew that handles both Financial Planning and Tax Planning.
    Accepts raw analysis data from Pixpoc and dynamically processes it.
    """
    
    def __init__(self, analysis_data: dict):
        """
        Initialize with raw analysis data from Pixpoc.
        No parsing needed - agents will understand the JSON dynamically.
        
        Args:
            analysis_data: Raw analysis data from Pixpoc callback
        """
        self.analysis_data = analysis_data
        self.agents_config = load_config(AGENTS_CONFIG)
        self.tasks_config = load_config(TASKS_CONFIG)
        
        # Get OpenAI API key from environment
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required. Please set it in your environment or .env file.")
        
        # Set environment variable for CrewAI (it reads from os.environ)
        os.environ["OPENAI_API_KEY"] = openai_api_key
        
        # Initialize OpenAI GPT-4o with proper tool support
        # CrewAI LLM reads OPENAI_API_KEY from environment automatically
        self.llm = LLM(
            model="gpt-4o",
            temperature=0.1
        )

    def create_agents(self):
        """Create all agents for comprehensive financial and tax planning"""
        
        # Financial Analysis Agent
        self.financial_analyst = Agent(
            role=self.agents_config['financial_analyst']['role'],
            goal=self.agents_config['financial_analyst']['goal'],
            backstory=self.agents_config['financial_analyst']['backstory'],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Tax Planning Agent
        self.tax_advisor = Agent(
            role=self.agents_config['tax_advisor']['role'],
            goal=self.agents_config['tax_advisor']['goal'],
            backstory=self.agents_config['tax_advisor']['backstory'],
            verbose=True,
            allow_delegation=False,
            tools=[tax_calculator_tool],
            llm=self.llm
        )
        
        # Investment Research Agent
        self.research_specialist = Agent(
            role=self.agents_config['research_specialist']['role'],
            goal=self.agents_config['research_specialist']['goal'],
            backstory=self.agents_config['research_specialist']['backstory'],
            verbose=True,
            allow_delegation=False,
            tools=[search_tool],
            llm=self.llm
        )
        
        # Strategy Advisor
        self.strategy_advisor = Agent(
            role=self.agents_config['strategy_advisor']['role'],
            goal=self.agents_config['strategy_advisor']['goal'],
            backstory=self.agents_config['strategy_advisor']['backstory'],
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        # Report Generator
        self.report_generator = Agent(
            role=self.agents_config['report_generator']['role'],
            goal=self.agents_config['report_generator']['goal'],
            backstory=self.agents_config['report_generator']['backstory'],
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def create_tasks(self):
        """Create all tasks for comprehensive planning"""
        
        # Convert analysis data to JSON string for agents
        analysis_json = json.dumps(self.analysis_data, indent=2)
        
        # Financial Analysis Task
        self.financial_analysis_task = Task(
            description=self.tasks_config['financial_analysis_task']['description'].format(
                analysis_data=analysis_json
            ),
            expected_output=self.tasks_config['financial_analysis_task']['expected_output'],
            agent=self.financial_analyst
        )
        
        # Tax Planning Task
        self.tax_planning_task = Task(
            description=self.tasks_config['tax_planning_task']['description'].format(
                analysis_data=analysis_json
            ),
            expected_output=self.tasks_config['tax_planning_task']['expected_output'],
            agent=self.tax_advisor
        )
        
        # Investment Research Task
        self.research_task = Task(
            description=self.tasks_config['research_task']['description'].format(
                analysis_data=analysis_json
            ),
            expected_output=self.tasks_config['research_task']['expected_output'],
            agent=self.research_specialist,
            context=[self.financial_analysis_task]
        )
        
        # Comprehensive Strategy Task
        self.strategy_task = Task(
            description=self.tasks_config['strategy_task']['description'],
            expected_output=self.tasks_config['strategy_task']['expected_output'],
            agent=self.strategy_advisor,
            context=[self.financial_analysis_task, self.tax_planning_task, self.research_task]
        )
        
        # Final Report Task
        self.report_task = Task(
            description=self.tasks_config['report_task']['description'].format(
                analysis_data=analysis_json
            ),
            expected_output=self.tasks_config['report_task']['expected_output'],
            agent=self.report_generator,
            context=[
                self.financial_analysis_task,
                self.tax_planning_task,
                self.research_task,
                self.strategy_task
            ]
        )

    def run(self):
        """Execute the comprehensive planning crew"""
        self.create_agents()
        self.create_tasks()
        
        crew = Crew(
            agents=[
                self.financial_analyst,
                self.tax_advisor,
                self.research_specialist,
                self.strategy_advisor,
                self.report_generator
            ],
            tasks=[
                self.financial_analysis_task,
                self.tax_planning_task,
                self.research_task,
                self.strategy_task,
                self.report_task
            ],
            verbose=True,
            process=Process.sequential
        )
        
        result = crew.kickoff()
        return result

