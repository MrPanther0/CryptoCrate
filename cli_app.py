import argparse
from file_encrypter import SecureFileStorage
import os

def main():
    parser = argparse.ArgumentParser(description="Secure File Storage System with AES-256 Encryption.")
    parser.add_argument("--key-file", default="storage.key", help="Path to the encryption key file.")
    parser.add_argument("--metadata-file", default="metadata.json", help="Path to the metadata file.")

    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Encrypt command
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file.")
    encrypt_parser.add_argument("input_file", help="Path to the file to encrypt.")
    encrypt_parser.add_argument("--output-dir", default="encrypted_files", help="Directory to save the encrypted file.")

    # Decrypt command
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt an encrypted file.")
    decrypt_parser.add_argument("encrypted_file", help="Path to the encrypted file to decrypt.")
    decrypt_parser.add_argument("--output-dir", default="decrypted_files", help="Directory to save the decrypted file.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all encrypted files and their metadata.")

    args = parser.parse_args()

    storage = SecureFileStorage(key_file=args.key_file, metadata_file=args.metadata_file)

    if args.command == "encrypt":
        if not os.path.exists(args.input_file):
            print(f"Error: Input file '{args.input_file}' not found.")
            return
        storage.encrypt_file(args.input_file, args.output_dir)
    elif args.command == "decrypt":
        if not os.path.exists(args.encrypted_file):
            print(f"Error: Encrypted file '{args.encrypted_file}' not found.")
            return
        storage.decrypt_file(args.encrypted_file, args.output_dir)
    elif args.command == "list":
        storage.list_encrypted_files()

if __name__ == "__main__":
    main()