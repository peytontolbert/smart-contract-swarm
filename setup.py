from setuptools import setup, find_packages

setup(
    name="smart_contract_swarm",
    version="0.1.0",
    packages=find_packages(include=['smart_contract_swarm', 'smart_contract_swarm.*']),
    install_requires=[
        "langchain-community>=0.0.1",
        "python-dotenv>=1.0.0",
        "openai>=1.3.0",
        "solders>=0.18.0",
        "solana-py>=0.30.2",
        "anchorpy>=0.18.0",
        "borsh-construct>=0.1.0",
        "construct-typing>=0.5.2,<0.6.0",
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
        "base58>=2.1.1"
    ],
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
) 