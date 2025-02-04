from langchain_community.chat_models import ChatOpenAI
from langchain.agents import Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, SystemMessage
from solana.rpc.api import Client
from solders.keypair import Keypair
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
            try:
                subprocess.run(["anchor", "--version"], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                raise RuntimeError("Anchor framework not found. Please install it with 'cargo install --git https://github.com/project-serum/anchor anchor-cli'")
            
            subprocess.run(["anchor", "init", str(self.program_dir)], check=True)
        
        # Update Anchor.toml with project configuration
        self.update_anchor_config(contract_name)
    
    def update_anchor_config(self, contract_name):
        config_path = self.program_dir / "Anchor.toml"
        if config_path.exists():
            with open(config_path, "r") as f:
                config = f.read()
            
            # Update program name
            config = config.replace("[programs.localnet]", f"[programs.localnet]\n{contract_name} = \"path/to/program\"")
            
            with open(config_path, "w") as f:
                f.write(config)
    
    def generate_contract_code(self, specs):
        """Generate the smart contract code based on specifications"""
        contract_path = self.program_dir / "programs" / "program" / "src" / "lib.rs"
        os.makedirs(contract_path.parent, exist_ok=True)
        with open(contract_path, "w") as f:
            f.write(specs["contract_code"])

class ContractSwarm:
    def __init__(self):
        self.agents = {
            "analyzer": SmartContractAgent(
                name="Requirement Analyzer",
                system_prompt="""You are a Solana smart contract requirements analyzer. 
                Analyze requirements and create detailed technical specifications for Solana blockchain.
                Focus on Anchor framework, Rust programming language, and Solana-specific features.
                Always include specific time periods (months, days) in the specifications."""
            ),
            "architect": SmartContractAgent(
                name="Contract Architect",
                system_prompt="""You are a Solana smart contract architect.
                Design smart contract architecture using Anchor framework and Rust.
                Include account structures, instructions, and state management following Solana best practices.
                Use PDAs (Program Derived Addresses) where appropriate."""
            ),
            "generator": SmartContractAgent(
                name="Code Generator",
                system_prompt="""You are a Solana smart contract code generator.
                Generate Rust code using the Anchor framework.
                Follow Solana programming model and security best practices.
                Include all necessary account validations and error handling."""
            ),
            "auditor": SmartContractAgent(
                name="Security Auditor",
                system_prompt="""You are a Solana smart contract security auditor.
                Audit code for vulnerabilities specific to Solana blockchain.
                Check for proper account validation, signer verification, and PDA usage.
                Verify compliance with Anchor framework best practices."""
            ),
            "tester": SmartContractAgent(
                name="Test Generator",
                system_prompt="""You are a Solana smart contract test generator.
                Create comprehensive test cases using Anchor's testing framework.
                Include tests for account validation, instruction execution, and error cases.
                Test PDA derivation and token operations where applicable."""
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
        
        try:
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
        except Exception as e:
            print(f"\nError during contract generation: {str(e)}")
            return contract_spec
    
    def build_and_test(self):
        """Build and test the generated smart contract"""
        try:
            # Check if Anchor is installed
            subprocess.run(["anchor", "--version"], check=True, capture_output=True)
            
            # Build the contract
            subprocess.run(["anchor", "build"], cwd=self.contract_generator.program_dir, check=True)
            
            # Run tests
            subprocess.run(["anchor", "test"], cwd=self.contract_generator.program_dir, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error during build/test: {e}")
            return False
        except FileNotFoundError:
            print("Anchor framework not found. Please install it with 'cargo install --git https://github.com/project-serum/anchor anchor-cli'")
            return False 