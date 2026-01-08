#!/usr/bin/env python3
"""
GitHub repository setup script for SeedFinder

This script helps create a GitHub repository and push the code.
Requires: gh CLI tool (https://cli.github.com/)
"""

import subprocess
import sys


def run_command(cmd, check=True):
    """Run shell command"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, 
                            capture_output=True, text=True)
        return result.stdout.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stderr.strip(), e.returncode


def check_gh_cli():
    """Check if GitHub CLI is installed"""
    stdout, returncode = run_command("gh --version", check=False)
    if returncode == 0:
        print(f"GitHub CLI found: {stdout}")
        return True
    else:
        print("GitHub CLI not found. Install from https://cli.github.com/")
        return False


def create_github_repo():
    """Create GitHub repository"""
    print("\nCreating GitHub repository...")
    
    # Create repo
    cmd = 'gh repo create seedfinder --public --source=. --remote=origin --push'
    stdout, returncode = run_command(cmd, check=False)
    
    if returncode == 0:
        print("Repository created and pushed successfully!")
        return stdout
    else:
        print(f"Error: {stdout}")
        return None


def setup_remote():
    """Set up remote repository if gh CLI not available"""
    print("\nManual setup instructions:")
    print("1. Create a new repository at https://github.com/new")
    print("   Repository name: seedfinder")
    print("   Description: Professional Minecraft seedfinding tool for mega-villages")
    print("   Make it public")
    print("   Do not initialize with README, .gitignore, or license")
    print()
    print("2. Add remote and push:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/seedfinder.git")
    print("   git branch -M main")
    print("   git push -u origin main")


def main():
    """Main function"""
    print("SeedFinder GitHub Repository Setup")
    print("=" * 50)
    
    # Check if we're in a git repo
    stdout, returncode = run_command("git rev-parse --git-dir", check=False)
    if returncode != 0:
        print("Error: Not in a git repository")
        sys.exit(1)
    
    print("Git repository found")
    
    # Check for GitHub CLI
    if check_gh_cli():
        # Try to create repo automatically
        result = create_github_repo()
        
        if not result:
            print("\nAutomatic setup failed. Using manual instructions...")
            setup_remote()
    else:
        setup_remote()
    
    print("\nSetup complete!")


if __name__ == "__main__":
    main()
