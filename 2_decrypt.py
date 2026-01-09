import os
import json
import base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

# Folder Configuration
PROTECTED_DATA_PATIENT = "Encrypted_Patient_data" # Encrypted data locatation
KEY_ROLE = "Role_Keys" # call the genearted keys

def decrypt_file():
    print("--- Begin Decryption File ---")

    # show exists protected files
    print(f"Files available: {os.listdir(PROTECTED_DATA_PATIENT)}")

    # make users to input file name (simulated they clicking file)
    filename = input("\nWhich file do you want to access? ").strip()
    file_path = os.path.join(PROTECTED_DATA_PATIENT, filename)

    # make system read role_key_vault from the selected file
    with open(file_path, "r") as f:
        metadata = json.load(f)
    
    role_key_vault = metadata["role_key_vault"] # keep the role key value
    
    # ask users for their key, in this case it was between ROLE_DOCTOR_private.pem or ROLE_NURSE_private.pem
    key_filename = input("Enter your Key File: ").strip() 
    key_path = os.path.join(KEY_ROLE, key_filename)

    if not os.path.exists(key_path): # in case no key found
        print("Error: Key file not found.")
        return

    # check the key is from Doctor or Nurse
    try:
        user_role = key_filename.replace("_private.pem", "")
    except:
        print("Error: Invalid key filename.") # just in case none role exists
        return

    # check if even the not Doctor or Nurse file does exists, but not have authorized.
    if user_role not in role_key_vault:
        print(f"Error: The key '{user_role}' in not in the Authorized lists")
        return

    # decrypt begin, after passing all checking conditions
    try: 
        # load the private key (.pem) from Role_Keys folder
        with open(key_path, "rb") as f:
            private_key = RSA.import_key(f.read())

        # decode the value from json
        encrypted_aes_key = base64.b64decode(role_key_vault[user_role])
        
        # unwrap with rsa decryption
        cipher_rsa = PKCS1_OAEP.new(private_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        
        # unlocking content
        nonce = base64.b64decode(metadata["nonce"])
        tag = base64.b64decode(metadata["tag"])
        ciphertext = base64.b64decode(metadata["ciphertext"]) 
        
        cipher_aes = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher_aes.decrypt_and_verify(ciphertext, tag) # the original text is here !!
        
        print("--- Decrypted Done ---")
        print(plaintext.decode('utf-8'))

    except Exception as e:
        print(f"Error: Decryption failed. {e}")


if __name__ == "__main__":
    decrypt_file()