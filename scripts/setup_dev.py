#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    print("Setting up development environment...")
    
    # Install the package in development mode
    print("\nInstalling package in development mode...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                  cwd=project_root, check=True)
    
    # Install test dependencies
    print("\nInstalling test dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "pytest-asyncio"], 
                  check=True)
    
    # Create necessary directories
    print("\nCreating project directories...")
    (project_root / "wallet").mkdir(exist_ok=True)
    (project_root / "program").mkdir(exist_ok=True)
    
    print("\nDevelopment environment setup complete!")

if __name__ == "__main__":
    main() 