#!/usr/bin/env python3
"""
JSON Syntax Fixer
This script attempts to fix common JSON syntax errors automatically.
"""

import json
import re
import os
import sys
import shutil
from pathlib import Path
from typing import Tuple, Optional

def remove_comments(json_string: str) -> str:
    """Remove JavaScript-style comments from JSON string."""
    # Remove single-line comments
    json_string = re.sub(r'//.*?$', '', json_string, flags=re.MULTILINE)
    # Remove multi-line comments
    json_string = re.sub(r'/\*.*?\*/', '', json_string, flags=re.DOTALL)
    return json_string

def fix_trailing_commas(json_string: str) -> str:
    """Remove trailing commas from JSON string."""
    # Remove trailing commas before closing brackets/braces
    json_string = re.sub(r',\s*([}\]])', r'\1', json_string)
    return json_string

def remove_bom(file_path: str) -> bool:
    """Remove UTF-8 BOM from file if present."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        if content.startswith(b'\xef\xbb\xbf'):
            # File has BOM, remove it
            with open(file_path, 'wb') as f:
                f.write(content[3:])
            return True
        return False
    except Exception:
        return False

def fix_empty_file(json_string: str) -> str:
    """Fix empty JSON files by adding minimal valid structure."""
    if not json_string.strip():
        return '{}'
    return json_string

def attempt_fix_json(file_path: str, backup: bool = True) -> Tuple[bool, str]:
    """
    Attempt to fix JSON syntax errors in a file.
    
    Returns:
        Tuple of (success, message)
    """
    try:
        # First check if file is already valid
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            json.loads(content)
            return True, "Already valid JSON"
        except json.JSONDecodeError:
            pass
        
        # Create backup if requested
        if backup:
            backup_path = f"{file_path}.backup"
            shutil.copy2(file_path, backup_path)
        
        # Apply fixes
        original_content = content
        
        # Fix 1: Remove BOM
        bom_removed = remove_bom(file_path)
        if bom_removed:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        # Fix 2: Handle empty files
        content = fix_empty_file(content)
        
        # Fix 3: Remove comments
        content = remove_comments(content)
        
        # Fix 4: Fix trailing commas
        content = fix_trailing_commas(content)
        
        # Try to parse the fixed content
        try:
            json.loads(content)
            
            # Save the fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            fixes = []
            if bom_removed:
                fixes.append("BOM removed")
            if not original_content.strip() and content.strip():
                fixes.append("empty file fixed")
            if '//' in original_content or '/*' in original_content:
                fixes.append("comments removed")
            if re.search(r',\s*[}\]]', original_content):
                fixes.append("trailing commas removed")
            
            return True, f"Fixed: {', '.join(fixes) if fixes else 'formatting normalized'}"
            
        except json.JSONDecodeError as e:
            # Restore backup if fix failed
            if backup and os.path.exists(f"{file_path}.backup"):
                shutil.move(f"{file_path}.backup", file_path)
            return False, f"Could not fix: {str(e)}"
            
    except Exception as e:
        return False, f"Error processing file: {str(e)}"

def main():
    """Main function to fix JSON files."""
    if len(sys.argv) < 2:
        print("Usage: python fix_json_syntax.py <file_or_directory> [--no-backup]")
        print("\nThis tool attempts to fix common JSON syntax errors:")
        print("  - Remove comments (// and /* */)")
        print("  - Remove trailing commas")
        print("  - Remove UTF-8 BOM")
        print("  - Fix empty files")
        print("\nBy default, backups are created with .backup extension")
        sys.exit(1)
    
    target = sys.argv[1]
    no_backup = "--no-backup" in sys.argv
    
    if os.path.isfile(target):
        # Fix single file
        success, message = attempt_fix_json(target, backup=not no_backup)
        if success:
            print(f"✅ {target}: {message}")
        else:
            print(f"❌ {target}: {message}")
    
    elif os.path.isdir(target):
        # Fix all JSON files in directory
        fixed_count = 0
        failed_count = 0
        
        for root, dirs, files in os.walk(target):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'venv', '__pycache__']]
            
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    success, message = attempt_fix_json(file_path, backup=not no_backup)
                    
                    if success and message != "Already valid JSON":
                        fixed_count += 1
                        print(f"✅ Fixed: {file_path}")
                        print(f"   {message}")
                    elif not success:
                        failed_count += 1
                        print(f"❌ Failed: {file_path}")
                        print(f"   {message}")
        
        print(f"\nSummary: {fixed_count} files fixed, {failed_count} files could not be fixed")
    
    else:
        print(f"Error: {target} is not a valid file or directory")
        sys.exit(1)

if __name__ == "__main__":
    main()
