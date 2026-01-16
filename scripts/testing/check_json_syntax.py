#!/usr/bin/env python3
"""
JSON Syntax Validator
This script finds and validates all JSON files in a directory tree,
reporting any syntax errors found.
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Tuple

def validate_json_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate a JSON file for syntax errors.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, ""
    except json.JSONDecodeError as e:
        return False, f"JSON Decode Error at line {e.lineno}, column {e.colno}: {e.msg}"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

def find_json_files(directory: str, exclude_dirs: List[str] = None) -> List[str]:
    """
    Find all JSON files in a directory tree.
    
    Args:
        directory: Root directory to search
        exclude_dirs: List of directory names to exclude
    
    Returns:
        List of JSON file paths
    """
    if exclude_dirs is None:
        exclude_dirs = ['node_modules', '.git', '__pycache__', 'venv', 'env', '.env']
    
    json_files = []
    
    for root, dirs, files in os.walk(directory):
        # Remove excluded directories from the search
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    
    return json_files

def main():
    """Main function to check JSON syntax in current directory or specified path."""
    # Get directory to check (default to current directory)
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"Checking JSON files in: {os.path.abspath(directory)}")
    print("-" * 80)
    
    # Find all JSON files
    json_files = find_json_files(directory)
    
    if not json_files:
        print("No JSON files found.")
        return
    
    print(f"Found {len(json_files)} JSON files. Validating...\n")
    
    # Track results
    valid_count = 0
    invalid_files = []
    
    # Validate each file
    for file_path in json_files:
        is_valid, error_msg = validate_json_file(file_path)
        
        if is_valid:
            valid_count += 1
        else:
            invalid_files.append((file_path, error_msg))
            print(f"❌ INVALID: {file_path}")
            print(f"   Error: {error_msg}")
            print()
    
    # Print summary
    print("-" * 80)
    print(f"\nSummary:")
    print(f"  Total JSON files checked: {len(json_files)}")
    print(f"  Valid files: {valid_count}")
    print(f"  Invalid files: {len(invalid_files)}")
    
    if invalid_files:
        print("\nFiles with syntax errors:")
        for file_path, error in invalid_files:
            print(f"  - {file_path}")
            
        # Offer to show common fixes
        print("\nCommon JSON syntax issues to check:")
        print("  1. Missing or extra commas (especially trailing commas)")
        print("  2. Unquoted keys or values")
        print("  3. Single quotes instead of double quotes")
        print("  4. Missing closing brackets or braces")
        print("  5. Invalid escape sequences in strings")
    else:
        print("\n✅ All JSON files are valid!")

if __name__ == "__main__":
    main()
