#!/usr/bin/env python3
from smart_contract_swarm.wallet import WalletManager

def main():
    print("Generating new Solana wallet...")
    wallet_manager = WalletManager()
    public_key, private_key = wallet_manager.generate_wallet()
    
    print(f"\nWallet generated successfully!")
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")
    print("\nCredentials have been saved to wallet/wallet.json and updated in .env")
    
    print("\nRequesting devnet SOL airdrop...")
    if wallet_manager.fund_wallet_devnet(public_key):
        print("Airdrop requested successfully!")
    
    print("\nWallet is ready for use with the smart contract swarm!")

if __name__ == "__main__":
    main() 