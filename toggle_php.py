#!/usr/bin/env python3
import subprocess
import sys
import re

# PHP versions sequence
PHP_VERSIONS = ["7.4", "8.2", "8.5"]

def run_command(cmd):
    """Run a shell command non-interactively."""
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode().strip()}")
        sys.exit(1)

def get_current_php_version():
    """Return the current PHP version as a string, e.g., '7.4'."""
    try:
        output = subprocess.check_output("php -v", shell=True, text=True)
        match = re.search(r"PHP (\d+\.\d+)", output)
        if match:
            return match.group(1)
        else:
            print("Unable to detect current PHP version.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("PHP is not installed or not in PATH.")
        sys.exit(1)

def toggle_php():
    current_version = get_current_php_version()
    print(f"Current PHP version: {current_version}")

    # Determine next version in sequence
    if current_version not in PHP_VERSIONS:
        print(f"PHP {current_version} is not managed by this script.")
        sys.exit(1)

    next_version = PHP_VERSIONS[(PHP_VERSIONS.index(current_version) + 1) % len(PHP_VERSIONS)]
    print(f"Toggling to PHP {next_version}...")

    # Switch PHP alternatives (non-interactive)
    run_command(f"sudo update-alternatives --set php /usr/bin/php{next_version}")

    # Disable current version in Apache, enable next version (non-interactive)
    run_command(f"sudo a2dismod php{current_version} -q")
    run_command(f"sudo a2enmod php{next_version} -q")

    # Restart Apache
    run_command("sudo systemctl restart apache2")

    print(f"Successfully switched to PHP {next_version}!")

if __name__ == "__main__":
    toggle_php()
