#!/usr/bin/env python3
"""
URL replacement tool for local testing of pyodide-pygame-demo.

Usage:
    python tools/replace_urls.py localhost    # Switch to localhost URLs
    python tools/replace_urls.py production   # Switch back to production URLs
    python tools/replace_urls.py status       # Check current state
"""

import sys
import re
from pathlib import Path

# Configuration
PRODUCTION_URL = "https://ryanking13.github.io/pyodide-pygame-demo"
LOCALHOST_URL = "http://localhost:8000"

# Files to process
HTML_PATTERNS = ["*.html", "**/*.html"]


def get_project_root():
    """Get the project root directory."""
    script_dir = Path(__file__).parent
    return script_dir.parent


def find_html_files(root_dir):
    """Find all HTML files in the project."""
    html_files = set()
    for pattern in HTML_PATTERNS:
        html_files.update(root_dir.glob(pattern))
    return sorted(html_files)


def replace_urls_in_file(file_path, old_url, new_url):
    """Replace URLs in a single file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Replace the URLs
        content = content.replace(old_url, new_url)
        
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def check_status(root_dir):
    """Check which URLs are currently in use."""
    html_files = find_html_files(root_dir)
    
    production_count = 0
    localhost_count = 0
    
    for file_path in html_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            if PRODUCTION_URL in content:
                production_count += 1
            if LOCALHOST_URL in content:
                localhost_count += 1
        except Exception:
            pass
    
    print(f"\nFound {len(html_files)} HTML files")
    print(f"Files with production URLs: {production_count}")
    print(f"Files with localhost URLs: {localhost_count}")
    
    if localhost_count > 0 and production_count == 0:
        print("\n[OK] Currently configured for LOCALHOST")
    elif production_count > 0 and localhost_count == 0:
        print("\n[OK] Currently configured for PRODUCTION")
    else:
        print("\n[WARNING] Mixed configuration detected!")
    
    return production_count, localhost_count


def switch_to_localhost(root_dir):
    """Switch all URLs to localhost."""
    print(f"Switching URLs to localhost ({LOCALHOST_URL})...")
    html_files = find_html_files(root_dir)
    
    modified_count = 0
    for file_path in html_files:
        if replace_urls_in_file(file_path, PRODUCTION_URL, LOCALHOST_URL):
            print(f"  [+] {file_path.relative_to(root_dir)}")
            modified_count += 1
    
    if modified_count == 0:
        print("  No files needed updating (already using localhost URLs)")
    else:
        print(f"\n[OK] Successfully modified {modified_count} file(s)")
        print(f"\nYou can now run a local server with:")
        print(f"  python -m http.server 8000")
        print(f"\nThen visit: http://localhost:8000/")


def switch_to_production(root_dir):
    """Switch all URLs back to production."""
    print(f"Switching URLs to production ({PRODUCTION_URL})...")
    html_files = find_html_files(root_dir)
    
    modified_count = 0
    for file_path in html_files:
        if replace_urls_in_file(file_path, LOCALHOST_URL, PRODUCTION_URL):
            print(f"  [+] {file_path.relative_to(root_dir)}")
            modified_count += 1
    
    if modified_count == 0:
        print("  No files needed updating (already using production URLs)")
    else:
        print(f"\n[OK] Successfully modified {modified_count} file(s)")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    root_dir = get_project_root()
    
    print(f"Project root: {root_dir}\n")
    
    if command == "localhost":
        switch_to_localhost(root_dir)
    elif command == "production":
        switch_to_production(root_dir)
    elif command == "status":
        check_status(root_dir)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()

