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

github_token = os.environ['GITHUB_TOKEN']
github_repository = os.environ['GITHUB_REPOSITORY']
github_actor = os.environ['GITHUB_ACTOR']

headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
}

try:
    with open('terraform_module_version.tf.json', 'r') as file:
        data = json.load(file)
        current_version = data['variable']['module_version']['default']
except Exception as e:
    print(f"Failed to read or parse terraform_module_version.tf.json: {e}")
    sys.exit(1)

try:
    response = requests.get('https://api.github.com/repos/blinqas/station/releases/latest')
    response.raise_for_status()
    latest_version = response.json()['tag_name']
    print("Release version " + latest_version + " found.")
except Exception as e:
    print(f"Failed to fetch latest release from GitHub: {e}")
    sys.exit(1)

if latest_version != current_version:
    print('Trying to update to version: ' + latest_version)
    data['variable']['module_version']['default'] = latest_version
    try:
        with open('terraform_module_version.tf.json', 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Failed to write updated version to terraform_module_version.tf.json: {e}")
        sys.exit(1)

    run_command(f'git config --global user.name "{github_actor}"')
    run_command(f'git config --global user.email "{github_actor}@users.noreply.github.com"')

    run_command('git add terraform_module_version.tf.json')

    status_output = subprocess.run('git status --porcelain', shell=True, stdout=subprocess.PIPE).stdout.decode().strip()
    if status_output:
        run_command(f'git commit -m "Update Station module version to {latest_version}"')
    else:
        print("No changes to commit.")

    branch_name = f"update-station-module-{latest_version}"

    run_command('git fetch --all')
    if check_existing_branch(branch_name, headers):
        print(f"Branch {branch_name} already exists. Checking out and updating it.")
        run_command(f'git checkout {branch_name}')
        run_command('git pull origin ' + branch_name)
    else:
        print(f"Creating new branch {branch_name}.")
        run_command(f'git checkout -b {branch_name}')

    if status_output:
        run_command(f'git push --set-upstream origin {branch_name}')

        if not check_existing_pull_request(branch_name, headers):
            payload = {
                'title': f'Update Terraform Module to {latest_version}',
                'body': 'This is an auto-generated PR to update the Station terraform module. See [changelog](https://github.com/blinqas/station/releases/latest) for more details',
                'head': branch_name,
                'base': 'trunk'
            }
            try:
                pr_response = requests.post(f'https://api.github.com/repos/{github_repository}/pulls', json=payload, headers=headers)
                pr_response.raise_for_status()
                print("Pull request created successfully.")
            except Exception as e:
                print(f"Failed to create pull request: {e}")
                sys.exit(1)
    else:
        print("No new changes to push.")

else:
    print("No new module version found. No updates required.")
