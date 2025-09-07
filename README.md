# CryptoCrate
Secure File Storage System with AES-256
A robust command-line interface (CLI) application developed in Python for encrypting and decrypting local files using AES-256 encryption. This system ensures data confidentiality and integrity through strong encryption and hash-based verification.
Features
AES-256 Encryption: Utilizes the cryptography library's Fernet implementation, which provides AES-256 encryption in CBC mode with a 128-bit IV and HMAC-SHA256 for authentication, offering a high level of security.
Automatic Key Management: Generates and securely stores a unique encryption key (storage.key) upon first use.
Metadata Storage: Securely stores essential file metadata (original filename, encryption timestamp, original file SHA256 hash) in metadata.json for integrity checks and file management.
File Integrity Verification: Prevents tampering by comparing the SHA256 hash of the decrypted file with the hash of the original file stored in the metadata.
Simple CLI: Easy-to-use command-line interface for encrypting, decrypting, and listing stored files.
Dedicated Output Directories: Encrypted and decrypted files are neatly organized into separate directories (encrypted_files/ and decrypted_files/).
Project Structure
code
Code
.
├── cli_app.py              # Main CLI application to interact with the storage system
├── file_encrypter.py       # Core encryption/decryption logic and file management
├── storage.key             # (Generated) Your AES encryption key - KEEP THIS SECURE!
├── metadata.json           # (Generated) Stores metadata for all encrypted files
├── encrypted_files/        # (Generated) Directory for encrypted files (.enc)
└── decrypted_files/        # (Generated) Directory for decrypted files
Getting Started
Prerequisites
Python 3.6+
cryptography library
Installation
Clone the repository:
code
Bash
git clone https://github.com/your-username/secure-file-storage.git
cd secure-file-storage
Install dependencies:
code
Bash
pip install cryptography
Usage
The application is controlled via cli_app.py with various subcommands.
1. Encrypting a File
To encrypt a file, use the encrypt command followed by the path to your input file.
code
Bash
python cli_app.py encrypt path/to/your/document.txt
This will create an encrypted_files/ directory (if it doesn't exist).
The encrypted file will be saved as encrypted_files/document.txt.enc.
A storage.key file will be generated (if it doesn't exist), which is crucial for decryption. Back up this key securely!
Metadata for the encrypted file will be added to metadata.json.
You can specify a different output directory for encrypted files:
code
Bash
python cli_app.py encrypt my_secret_report.pdf --output-dir my_vault
2. Decrypting a File
To decrypt an encrypted file, use the decrypt command followed by the path to the .enc file.
code
Bash
python cli_app.py decrypt encrypted_files/document.txt.enc
This will create a decrypted_files/ directory (if it doesn't exist).
The decrypted file will be saved as decrypted_files/document.txt.
An integrity check will be performed against the original file's hash stored in metadata.json. You will be notified if any tampering or corruption is detected.
You can specify a different output directory for decrypted files:
code
Bash
python cli_app.py decrypt my_vault/my_secret_report.pdf.enc --output-dir retrieved_documents
3. Listing Encrypted Files
To view a list of all files that have been encrypted and their associated metadata, use the list command.
code
Bash
python cli_app.py list
This will display details like the original filename, encryption timestamp, original SHA256 hash, and the path to the encrypted file.
Important Security Notes
Key Management is CRITICAL: The storage.key file is your master key. Anyone with access to this file can decrypt all your encrypted files.
Keep it absolutely secure.
Back it up in a safe, separate location. If you lose this key, your encrypted files cannot be recovered.
Never share this key.
Metadata (metadata.json): While not as critical as the key, this file contains information about your encrypted files, including their original names and hashes. Keep it secure to maintain the integrity of your system.
File Hashes: The SHA256 hash is calculated before encryption. This hash is used to verify the integrity of the file after decryption. If the decrypted file's hash doesn't match the stored original hash, it indicates that the file was either corrupted during storage/transmission or tampered with.
How it Works (Technical Details)
The system leverages the cryptography library's Fernet implementation:
Key Derivation: Fernet keys are URL-safe base64-encoded 32-byte (256-bit) keys.
Encryption Process:
A unique Initialization Vector (IV) is generated for each encryption operation.
The plaintext is encrypted using AES-256 in CBC (Cipher Block Chaining) mode with the key and IV.
A SHA256 HMAC (Hash-based Message Authentication Code) is generated over the IV and ciphertext using a separate MAC key (derived from the master Fernet key).
The IV, timestamp, ciphertext, and HMAC are concatenated and then base64-encoded to form the final Fernet token.
Decryption Process:
The base64-encoded token is decoded.
The HMAC is verified. If it doesn't match, the decryption fails, indicating tampering.
The timestamp is checked for freshness (optional by Fernet, but part of its design).
The ciphertext is decrypted using AES-256 CBC with the key and IV.
Integrity Verification (Application Level): In addition to Fernet's internal HMAC verification, this application calculates the SHA256 hash of the original plaintext file before encryption and stores it in metadata.json. Upon decryption, it calculates the SHA256 hash of the newly decrypted file and compares it to the stored hash. This provides an extra layer of confidence that the data retrieved matches the data that was originally encrypted.
