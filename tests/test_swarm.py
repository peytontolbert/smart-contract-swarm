import pytest
from pathlib import Path
import json
import os
import subprocess
from smart_contract_swarm import ContractSwarm, SmartContractAgent, ContractGenerator

@pytest.fixture
def swarm():
    return ContractSwarm()

@pytest.fixture
def sample_requirements():
    return """
    Create a token vesting contract with the following features:
    - Linear vesting over 12 months
    - Cliff period of 3 months
    - Emergency pause functionality
    - Admin controls for vesting schedule modification
    """

def is_anchor_installed():
    try:
        subprocess.run(["anchor", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def test_requirement_analyzer(swarm, sample_requirements):
    """Test requirement analysis phase"""
    specs = swarm.agents["analyzer"].execute(sample_requirements)
    assert specs is not None
    assert isinstance(specs, str)
    assert "solana" in specs.lower()
    assert "anchor" in specs.lower()
    assert "months" in specs.lower()
    assert "vesting" in specs.lower()

def test_contract_architect(swarm):
    """Test contract architecture design phase"""
    sample_specs = """
    Technical Specifications for Solana Smart Contract:
    1. Token Vesting Schedule
       - Implementation of linear vesting over 12-month period
       - 3-month cliff implementation using Solana timestamps
    2. Access Control
       - Admin PDA for schedule modifications
       - Emergency pause functionality using program state
    """
    architecture = swarm.agents["architect"].execute(sample_specs)
    assert architecture is not None
    assert isinstance(architecture, str)
    assert "struct" in architecture.lower()
    assert "pda" in architecture.lower()
    assert "account" in architecture.lower()

def test_code_generator(swarm):
    """Test smart contract code generation"""
    sample_architecture = """
    Contract Architecture:
    1. State accounts:
       - VestingSchedule
       - UserVesting
    2. Instructions:
       - initialize_vesting
       - claim_tokens
       - pause_vesting
       - modify_schedule
    """
    code = swarm.agents["generator"].execute(sample_architecture)
    assert code is not None
    assert isinstance(code, str)
    assert "use anchor_lang" in code.lower()
    assert "#[program]" in code
    assert "pub struct" in code.lower()
    assert "pub fn" in code.lower()

def test_security_auditor(swarm):
    """Test security audit functionality"""
    sample_code = """
    use anchor_lang::prelude::*;
    
    #[program]
    pub mod vesting_contract {
        use super::*;
        
        pub fn initialize_vesting(ctx: Context<InitializeVesting>) -> Result<()> {
            Ok(())
        }
    }
    """
    audit_result = swarm.agents["auditor"].execute(sample_code)
    assert audit_result is not None
    assert isinstance(audit_result, str)
    assert "security" in audit_result.lower()
    assert "validation" in audit_result.lower()

def test_test_generator(swarm):
    """Test the test case generation"""
    sample_code = """
    use anchor_lang::prelude::*;
    
    #[program]
    pub mod vesting_contract {
        use super::*;
        
        pub fn initialize_vesting(ctx: Context<InitializeVesting>) -> Result<()> {
            Ok(())
        }
    }
    """
    test_cases = swarm.agents["tester"].execute(sample_code)
    assert test_cases is not None
    assert isinstance(test_cases, str)
    assert "test" in test_cases.lower()
    assert "#[test]" in test_cases

@pytest.mark.skipif(not is_anchor_installed(), reason="Anchor framework not installed")
def test_contract_generator():
    """Test contract generator functionality"""
    generator = ContractGenerator()
    
    # Test project creation
    generator.create_anchor_project("test_contract")
    assert generator.program_dir.exists()
    
    # Test contract code generation
    specs = {
        "contract_code": """
        use anchor_lang::prelude::*;
        
        #[program]
        pub mod vesting_contract {
            use super::*;
            
            pub fn initialize_vesting(ctx: Context<InitializeVesting>) -> Result<()> {
                Ok(())
            }
        }
        """
    }
    generator.generate_contract_code(specs)
    contract_path = generator.program_dir / "programs" / "program" / "src" / "lib.rs"
    assert contract_path.exists()

@pytest.mark.skipif(not is_anchor_installed(), reason="Anchor framework not installed")
def test_full_contract_generation(swarm, sample_requirements):
    """Test the complete contract generation process"""
    result = swarm.process_contract_request(sample_requirements)
    
    assert result["requirements"] == sample_requirements
    assert result["technical_specs"] is not None
    assert result["architecture"] is not None
    assert result["contract_code"] is not None
    assert result["security_audit"] is not None
    assert result["test_cases"] is not None
    
    # Check if Anchor project was created
    assert swarm.contract_generator.program_dir.exists()
    contract_path = swarm.contract_generator.program_dir / "programs" / "program" / "src" / "lib.rs"
    assert contract_path.exists() 