import os # Make Window OS know we gonna create Folder and File
from Crypto.PublicKey import RSA # Libraly from out-source for RSA Maths

# Locates Folder for Role Key
KEY_ROLE = "Role_Keys" 

def setup_system():
    print("--- HOSPITAL ROLE SYSTEM SETUP ---")
    
    # 1. Create Folder for ROLE keys
    os.makedirs(KEY_ROLE, exist_ok=True)

    # 2. Generate Different Two ROLE Keys
    attributes = ["ROLE_DOCTOR", "ROLE_NURSE"]
    
    for attr in attributes:
        print(f"Generating RSA Keypair: {attr}")
        key = RSA.generate(2048) # We will get unique Key Pair for each Roles
        
        # Private key: use to decrrypt data 
        with open(os.path.join(KEY_ROLE, f"{attr}_private.pem"), "wb") as f:
            f.write(key.export_key())
            
        # Public key: use to encrypt data
        with open(os.path.join(KEY_ROLE, f"{attr}_public.pem"), "wb") as f:
            f.write(key.publickey().export_key())

    print("--- Setup System Done ---")


if __name__ == "__main__":
    setup_system()