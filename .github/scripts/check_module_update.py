import json
import requests
import os
import subprocess
import sys

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.cmd}")
        print(f"Error message: {e.stderr.decode()}")
        sys.exit(1)

def validate_env_variables():
    required_vars = ['GITHUB_TOKEN', 'GITHUB_REPOSITORY', 'GITHUB_ACTOR']
    missing_vars = [var for var in required_vars if var not in os.environ]
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

validate_env_variables()

# Load environment variables
github_token = os.environ['GITHUB_TOKEN']
github_repository = os.environ['GITHUB_REPOSITORY']
github_actor = os.environ['GITHUB_ACTOR']

# Load current module version from .tf.json file
try:
    with open('terraform_module_version.tf.json', 'r') as file:
        data = json.load(file)
        current_version = data['variable']['module_version']['default']

except Exception as e:
    print(f"Failed to read or parse terraform_module_version.tf.json: {e}")
    sys.exit(1)

# Fetch latest release version from GitHub
try:
    response = requests.get('https://api.github.com/repos/blinqas/station/releases/latest')
    response.raise_for_status()
    latest_version = response.json()['tag_name']
    print("Release version " + latest_version + " found.")
except Exception as e:
    print(f"Failed to fetch latest release from GitHub: {e}")
    sys.exit(1)

# Compare and update file if new version is found
if latest_version != current_version:
    print('Trying to update to version: ' + latest_version)
    data['variable']['module_version']['default'] = latest_version
    try:
        with open('terraform_module_version.tf.json', 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Failed to write updated version to terraform_module_version.tf.json: {e}")
        sys.exit(1)

    # Setting up Git configuration
    run_command(f'git config --global user.name "{github_actor}"')
    run_command(f'git config --global user.email "{github_actor}@users.noreply.github.com"')

    # Creating a new branch
    branch_name = f"update-terraform-module-{latest_version}"
    run_command(f'git checkout -b {branch_name}')

    # Committing the changes
    run_command('git add terraform_module_version.tf.json')
    run_command(f'git commit -m "Update Terraform module version to {latest_version}"')

    # Pushing the changes
    run_command(f'git push --set-upstream origin {branch_name}')

    # Creating a pull request
    # Creating a pull request
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    payload = {
        'title': f'Update Terraform Module to {latest_version}',
        'body': 'This is an auto-generated PR with the updated Terraform module version.',
        'head': branch_name,
        'base': 'trunk'  # Change to your default branch if different
    }
    try:
        pr_response = requests.post(f'https://api.github.com/repos/{github_repository}/pulls', json=payload, headers=headers)
        pr_response.raise_for_status()
        print("Pull request created successfully.")
    except Exception as e:
        print(f"Failed to create pull request: {e}")
        sys.exit(1)

else:
    print("No new module version found. No updates required.")
