"""
Fix Unicode characters in all Python files for Windows console compatibility
"""

import os
import re
from pathlib import Path

# Unicode replacements
REPLACEMENTS = {
    '[LOAD]': '[LOAD]',
    '[ERROR]': '[ERROR]',
    '[OK]': '[OK]',
    '[WARN]': '[WARN]',
    '[START]': '[START]',
    '[ENERGY]': '[ENERGY]',
    '[TRANSPORT]': '[TRANSPORT]',
    '[SAVE]': '[SAVE]',
    '[STATS]': '[STATS]',
    '[DIR]': '[DIR]',
    '->': '->',
    '2': '2',
    '*': '*',
}

def fix_file(file_path):
    """Fix Unicode characters in a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for unicode_char, replacement in REPLACEMENTS.items():
        content = content.replace(unicode_char, replacement)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {file_path.name}")
        return True
    return False

def fix_all_files(base_dir):
    """Fix all Python files in the directory"""
    base_path = Path(base_dir)
    fixed_count = 0
    
    for py_file in base_path.rglob('*.py'):
        if fix_file(py_file):
            fixed_count += 1
    
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[2] / "data"
    print(f"Fixing Unicode characters in: {base_dir}\n")
    fix_all_files(base_dir)
    print("\nDone!")
