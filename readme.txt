Assessment Cover Sheet 2025/26
Module code and title - 6G7V0033 Cryptography and Applications 
Assessment set by - Safiullah Khan 
Assessment ID - 1CWK100 
Assessment title - Cryptographic Algorithm Analysis and Software Implementation 
Type - Individual 
Hand-in deadline - 9 Jan 2026, 9 pm.
Hand-in format and mechanism - Video recording of a PowerPoint Presentation and Implementation demonstration to be uploaded to Moodle

---

Natthapong Thunguan, 25937641

Github: https://github.com/NatthapongPop/6G7V0033-1CWK100-Cryptography-25937641

---

 >>>>>> steps on BASH


python -m venv venv
    >> create virtual environment

source venv/Scripts/activate
    >> use VM

pip install cryptography
pip install pycryptodome
    >> install cryp libarly from out source


pip list
pip freeze
    >> check installed libarly

----------------------------------------------

--- Story ---

1. The Roles have been set, contains with Doctor and Nurse roles. as Role base access control.

2. The Patient for this silumated name Fern, Hospital will have the reable file as patient_info_Fern.txt and schedule_Fern.txt

3. from "0_hospital_setup.py" command, The Doctor and Nurse will get their seperate key to access Patient Fern Data

4. from "1_encrypt_data.py" command, The Patient Fern Data will be automated Encrypted to be unreadable 
    by Locking the Content with AES-GCM, then Applying Role Access Control with RSA Key Wrapped
    which requires the key from Doctor or Nurse, to access the protected data.

5. from "2_decrypt.py" command, The System will ask users which file to selected,
    after selected the files, it will ask users again for user private key (in this case we use .pem file)
    after user provided thier .pem file already, system will checking again.
        If the file name is incorrects, Access Denined
        If the details in the file is incorrect, Access Denined
        But if the Everythings does Correctly, System will begin Decryption and Provided the Plaintext for Users.

