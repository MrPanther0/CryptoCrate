# CryptoCrate

Secure File Storage System with AES-256

A robust command-line interface (CLI) application developed in Python for encrypting and decrypting local files using AES-256 encryption. This system ensures data confidentiality and integrity through strong encryption and hash-based verification.

## Features

*   **AES-256 Encryption:** Utilizes the `cryptography` library's Fernet implementation, which provides AES-256 encryption in CBC mode with a 128-bit IV and HMAC-SHA256 for authentication, offering a high level of security.
*   **Automatic Key Management:** Generates and securely stores a unique encryption key (`storage.key`) upon first use.
*   **Metadata Storage:** Securely stores essential file metadata (original filename, encryption timestamp, original file SHA256 hash) in `metadata.json` for integrity checks and file management.
*   **File Integrity Verification:** Prevents tampering by comparing the SHA256 hash of the decrypted file with the hash of the original file stored in the metadata.
*   **Simple CLI:** Easy-to-use command-line interface for encrypting, decrypting, and listing stored files.
*   **Dedicated Output Directories:** Encrypted and decrypted files are neatly organized into separate directories (`encrypted_files/` and `decrypted_files/`).

## Project Structure
- `cli_app.py` - Main CLI application to interact with the storage system
- `file_encrypter.py` - Core encryption/decryption logic and file management
- `storage.key` - (Generated) Your AES encryption key - KEEP THIS SECURE!
- `metadata.json` - (Generated) Stores metadata for all encrypted files
- `encrypted_files/` - (Generated) Directory for encrypted files (.enc)
- `decrypted_files/` - (Generated) Directory for decrypted files
