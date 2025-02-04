from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, SystemMessage
from solana.rpc.api import Client
from solana.keypair import Keypair
from anchorpy import Provider, Program
from pathlib import Path
import json
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Solana client
client = Client(os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com"))

# Initialize the language model
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

class SmartContractAgent:
    def __init__(self, name, system_prompt, tools=None):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm
        self.tools = tools or []
        self.memory = ConversationBufferMemory(memory_key="chat_history")
    
    def execute(self, input_data):
        """Execute the agent's task"""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=str(input_data))
        ]
        response = self.llm.generate([messages])
        return response.generations[0][0].text

class ContractGenerator:
    def __init__(self):
        self.program_dir = Path("program")
    
    def create_anchor_project(self, contract_name):
        """Initialize a new Anchor project"""
        if not self.program_dir.exists():
            subprocess.run(["anchor", "init", str(self.program_dir)], check=True)
        
        # Update Anchor.toml with project configuration
        self.update_anchor_config(contract_name)
    
    def update_anchor_config(self, contract_name):
        config_path = self.program_dir / "Anchor.toml"
        # Update Anchor.toml configuration here
        pass
    
    def generate_contract_code(self, specs):
        """Generate the smart contract code based on specifications"""
        contract_path = self.program_dir / "programs" / "program" / "src" / "lib.rs"
        with open(contract_path, "w") as f:
            f.write(specs["contract_code"])

class ContractSwarm:
    def __init__(self):
        self.agents = {
            "analyzer": SmartContractAgent(
                name="Requirement Analyzer",
                system_prompt="Analyze smart contract requirements and create detailed technical specifications."
            ),
            "architect": SmartContractAgent(
                name="Contract Architect",
                system_prompt="Design Solana smart contract architecture with data structures and interfaces."
            ),
            "generator": SmartContractAgent(
                name="Code Generator",
                system_prompt="Generate Rust code for Solana smart contract using Anchor framework."
            ),
            "auditor": SmartContractAgent(
                name="Security Auditor",
                system_prompt="Audit smart contract code for security vulnerabilities and Solana best practices."
            ),
            "tester": SmartContractAgent(
                name="Test Generator",
                system_prompt="Generate comprehensive test cases for Solana smart contract validation."
            )
        }
        self.contract_generator = ContractGenerator()
    
    def process_contract_request(self, user_requirements):
        """Process a smart contract request through the agent workflow"""
        contract_spec = {
            "requirements": user_requirements,
            "technical_specs": None,
            "architecture": None,
            "contract_code": None,
            "security_audit": None,
            "test_cases": None
        }
        
        # 1. Analyze requirements
        print("\nAnalyzing requirements...")
        contract_spec["technical_specs"] = self.agents["analyzer"].execute(user_requirements)
        
        # 2. Design architecture
        print("\nDesigning contract architecture...")
        contract_spec["architecture"] = self.agents["architect"].execute(contract_spec["technical_specs"])
        
        # 3. Generate contract code
        print("\nGenerating smart contract code...")
        contract_spec["contract_code"] = self.agents["generator"].execute(contract_spec["architecture"])
        
        # 4. Security audit
        print("\nPerforming security audit...")
        contract_spec["security_audit"] = self.agents["auditor"].execute(contract_spec["contract_code"])
        
        # 5. Generate tests
        print("\nGenerating test cases...")
        contract_spec["test_cases"] = self.agents["tester"].execute(contract_spec["contract_code"])
        
        # 6. Create and build contract
        print("\nCreating Anchor project...")
        self.contract_generator.create_anchor_project("smart_contract")
        self.contract_generator.generate_contract_code(contract_spec)
        
        # 7. Build and test
        if self.build_and_test():
            print("\nSmart contract successfully created and validated!")
        else:
            print("\nWarning: Contract validation failed. Please review the output.")
        
        return contract_spec
    
    def build_and_test(self):
        """Build and test the generated smart contract"""
        try:
            # Build the contract
            subprocess.run(["anchor", "build"], cwd=self.contract_generator.program_dir, check=True)
            
            # Run tests
            subprocess.run(["anchor", "test"], cwd=self.contract_generator.program_dir, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error during build/test: {e}")
            return False

# Initialize the swarm
swarm = ContractSwarm()

# Example usage
if __name__ == "__main__":
    user_requirements = """
    Create a token vesting contract with the following features:
    - Linear vesting over 12 months
    - Cliff period of 3 months
    - Emergency pause functionality
    - Admin controls for vesting schedule modification
    """
    
    result = swarm.process_contract_request(user_requirements) 