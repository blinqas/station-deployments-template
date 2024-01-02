import json
import requests
import os
import subprocess
import sys
from datetime import datetime

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

def check_existing_branch(branch_name, headers):
    response = requests.get(f'https://api.github.com/repos/{github_repository}/git/ref/heads/{branch_name}', headers=headers)
    return response.status_code == 200

def check_existing_pull_request(branch_name, headers):
    prs = requests.get(f'https://api.github.com/repos/{github_repository}/pulls?state=open', headers=headers)
    if prs.status_code == 200:
        for pr in prs.json():
            if pr['head']['ref'] == branch_name:
                print(f"Pull request already exists for branch {branch_name}")
                return True
    return False

validate_env_variables()

# Load environment variables
github_token = os.environ['GITHUB_TOKEN']
github_repository = os.environ['GITHUB_REPOSITORY']
github_actor = os.environ['GITHUB_ACTOR']

# Headers for GitHub API requests
headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
}

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
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    branch_name = f"update-terraform-module-{latest_version}-{current_time}"
    
    # Check if the branch already exists
    if check_existing_branch(branch_name, headers):
        print(f"Branch {branch_name} already exists.")
        if check_existing_pull_request(branch_name, headers):
            print("No new pull request created as an existing one is open.")
            sys.exit(0)
        else:
            print("Updating existing branch.")

    if not check_existing_pull_request(branch_name, headers):
        run_command(f'git checkout -b {branch_name}')

        # Committing the changes
        run_command('git add terraform_module_version.tf.json')
        run_command(f'git commit -m "Update Terraform module version to {latest_version}"')

        # Pushing the changes
        run_command(f'git push --set-upstream origin {branch_name}')

        # Creating a pull request
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
