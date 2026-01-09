import os # Make Window OS know we gonna create Folder and File
import json
import base64
from Crypto.Cipher import AES, PKCS1_OAEP # PKCS1_OAEP -> Auto add random padding
from Crypto.PublicKey import RSA # Libraly from out-source for RSA Maths
from Crypto.Random import get_random_bytes # Libraly to generates random bytes

# Locates Folder
UNPROTECT_DATA_PATIENT = "UnProtected_Patient_Data" # already mockup files
OUTPUT = "Encrypted_Patient_data" # Encrypted data will locate there
KEY_ROLE = "Role_Keys" # call the genearted keys

# As we use Role based encryption, each file wil contains with specific access roles
ACCESS_POLICY = {
    "patient_info_Fern.txt": ["ROLE_DOCTOR"], # only Doctor
    "schedule_Fern.txt":     ["ROLE_DOCTOR", "ROLE_NURSE"] # Doctor and Nurse
}


def encrypt_files():
    print("--- Begin Encrypts File ---")
    
    os.makedirs(OUTPUT, exist_ok=True)

    # Loop a lists in ACCESS_POLICY
    for filename, required_roles in ACCESS_POLICY.items():
        print(f"File: {filename}") # just show what file is processing
        print(f"Roles: {required_roles}") # just show what role is processing
        
        # Read the UnProtect Patien Data
        file_path = os.path.join(UNPROTECT_DATA_PATIENT, filename)
        with open(file_path, "rb") as f:
            file_data = f.read()

        aes_key = get_random_bytes(32) # Generate AES KEY
        
        # We use GCM Mode to Encrypt Data
        cipher_aes = AES.new(aes_key, AES.MODE_GCM) # make new cipher object to get AES values
        ciphertext, tag = cipher_aes.encrypt_and_digest(file_data) # ciphertext get patient data, tag get calculated hash of patient data

        encrypted_keys_vault = {}
        
        for role in required_roles:
            # Loads public key of each Roles
            key_path = os.path.join(KEY_ROLE, f"{role}_public.pem")
            with open(key_path, "rb") as f:
                role_public_key = RSA.import_key(f.read())
            
            # Wrap the AES key
            cipher_rsa = PKCS1_OAEP.new(role_public_key) # Keep padded results with Role
            wrapped_key = cipher_rsa.encrypt(aes_key) # Only the roles with correct private key can unlock aes_key reulsts, after this
            
            # save warpped key as a roles that can have access
            encrypted_keys_vault[role] = base64.b64encode(wrapped_key).decode('utf-8')

        # we save a JSON file containing the locked data + the locked keys
        metadata = {
            "filename": filename,
            "policy": required_roles,
            "nonce": base64.b64encode(cipher_aes.nonce).decode('utf-8'),
            "tag": base64.b64encode(tag).decode('utf-8'),
            "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
            "role_key_vault": encrypted_keys_vault
        }
        
        out_name = filename + ".locked"
        with open(os.path.join(OUTPUT, out_name), "w") as f:
            json.dump(metadata, f, indent=4)
            
        print(f"Done Encrypted to: {out_name}")


if __name__ == "__main__":
    encrypt_files()