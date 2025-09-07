import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import json
import datetime

class SecureFileStorage:
    def __init__(self, key_file="storage.key", metadata_file="metadata.json"):
        self.key_file = key_file
        self.metadata_file = metadata_file
        self._key = self._load_or_generate_key()
        self.fernet = Fernet(self._key)
        self.metadata = self._load_metadata()

    def _load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            print(f"Generated new encryption key and saved to {self.key_file}")
        return key

    def _load_metadata(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r") as f:
                return json.load(f)
        return {}

    def _save_metadata(self):
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=4)

    def _calculate_hash(self, filepath):
        hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.finalize().hex()

    def encrypt_file(self, input_filepath, output_dir="encrypted_files"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        original_filename = os.path.basename(input_filepath)
        encrypted_filename = original_filename + ".enc"
        output_filepath = os.path.join(output_dir, encrypted_filename)

        print(f"Encrypting {input_filepath}...")
        with open(input_filepath, "rb") as f:
            original_data = f.read()

        encrypted_data = self.fernet.encrypt(original_data)

        with open(output_filepath, "wb") as f:
            f.write(encrypted_data)

        original_file_hash = self._calculate_hash(input_filepath)

        self.metadata[encrypted_filename] = {
            "original_filename": original_filename,
            "encryption_time": datetime.datetime.now().isoformat(),
            "original_file_hash_sha256": original_file_hash,
            "encrypted_file_path": output_filepath
        }
        self._save_metadata()
        print(f"File encrypted and saved to {output_filepath}")
        print("Metadata updated.")
        return output_filepath

    def decrypt_file(self, encrypted_filepath, output_dir="decrypted_files"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        encrypted_filename = os.path.basename(encrypted_filepath)
        metadata_entry = self.metadata.get(encrypted_filename)

        if not metadata_entry:
            print(f"Error: No metadata found for {encrypted_filename}. Cannot decrypt securely.")
            return None

        original_filename = metadata_entry["original_filename"]
        output_filepath = os.path.join(output_dir, original_filename)

        print(f"Decrypting {encrypted_filepath}...")
        with open(encrypted_filepath, "rb") as f:
            encrypted_data = f.read()

        try:
            decrypted_data = self.fernet.decrypt(encrypted_data)
        except Exception as e:
            print(f"Decryption failed: {e}")
            return None

        with open(output_filepath, "wb") as f:
            f.write(decrypted_data)

        # Verify hash
        decrypted_file_hash = self._calculate_hash(output_filepath)
        stored_original_hash = metadata_entry["original_file_hash_sha256"]

        if decrypted_file_hash == stored_original_hash:
            print(f"File decrypted successfully to {output_filepath}")
            print("Integrity check passed: Decrypted file hash matches original.")
        else:
            print(f"WARNING: Integrity check failed for {output_filepath}!")
            print(f"Stored original hash: {stored_original_hash}")
            print(f"Decrypted file hash:  {decrypted_file_hash}")
            print("The decrypted file may have been tampered with or corrupted.")
        
        return output_filepath

    def list_encrypted_files(self):
        if not self.metadata:
            print("No files have been encrypted yet.")
            return

        print("\n--- Encrypted Files ---")
        for enc_filename, details in self.metadata.items():
            print(f"  Encrypted: {enc_filename}")
            print(f"    Original: {details['original_filename']}")
            print(f"    Time: {details['encryption_time']}")
            print(f"    Hash (SHA256): {details['original_file_hash_sha256']}")
            print(f"    Path: {details['encrypted_file_path']}")
            print("-" * 25)
        print("-----------------------\n")