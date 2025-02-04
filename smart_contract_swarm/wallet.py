from solders.keypair import Keypair
from solana.rpc.api import Client
from pathlib import Path
import json
import base58
import os
from dotenv import load_dotenv

class WalletManager:
    def __init__(self):
        load_dotenv()
        self.client = Client(os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com"))
        self.wallet_dir = Path("wallet")
    
    def generate_wallet(self):
        """Generate a new Solana wallet and save credentials"""
        # Generate new keypair
        keypair = Keypair()
        
        # Get public and private keys
        public_key = str(keypair.pubkey())
        private_key = base58.b58encode(keypair.secret()).decode('ascii')
        
        # Create wallet directory if it doesn't exist
        self.wallet_dir.mkdir(exist_ok=True)
        
        # Save keys to files
        with open(self.wallet_dir / "wallet.json", "w") as f:
            json.dump({
                "public_key": public_key,
                "private_key": private_key
            }, f, indent=4)
        
        # Update .env file with wallet info
        self._update_env_file(public_key, private_key)
        
        return public_key, private_key
    
    def _update_env_file(self, public_key, private_key):
        """Update .env file with wallet information"""
        env_path = Path(".env")
        if env_path.exists():
            with open(env_path, "r") as f:
                env_contents = f.read()
        else:
            env_contents = ""
        
        # Add or update wallet configuration in .env
        with open(env_path, "a") as f:
            if "WALLET_PUBLIC_KEY" not in env_contents:
                f.write(f"\nWALLET_PUBLIC_KEY={public_key}")
            if "WALLET_PRIVATE_KEY" not in env_contents:
                f.write(f"\nWALLET_PRIVATE_KEY={private_key}")
    
    def fund_wallet_devnet(self, public_key):
        """Request airdrop for the wallet on devnet"""
        try:
            # Request 2 SOL airdrop (2 billion lamports)
            result = self.client.request_airdrop(public_key, 2000000000)
            print(f"Airdrop requested: {result['result']}")
            return True
        except Exception as e:
            print(f"Error requesting airdrop: {e}")
            return False 