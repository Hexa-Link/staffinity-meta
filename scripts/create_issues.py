import os
import sys
import yaml
import requests

# --- CONFIGURATION ---
# IMPORTANT: Change 'Hexa-Link' to the exact case-sensitive name
# of your organization on GitHub.
GITHUB_ORG = 'Hexa-Link' 
# ---------------------

def create_sprint_issues(sprint_file_path):
    """
    Reads a YAML sprint definition file and creates the corresponding issues
    in GitHub repositories using the API.
    """
    print(f"Starting issue creation process from file: '{sprint_file_path}'")

    try:
        with open(sprint_file_path, 'r', encoding='utf-8') as file:
            sprint_data = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"FATAL ERROR: Could not find file '{sprint_file_path}'. Verify that the path is correct.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"FATAL ERROR: The YAML file '{sprint_file_path}' has a format error: {e}")
        sys.exit(1)

    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("FATAL ERROR: The GITHUB_TOKEN environment variable is not configured. The script cannot authenticate.")
        sys.exit(1)

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    issues_in_file = sprint_data.get('issues', [])
    print(f"Found {len(issues_in_file)} issues to create.")
    print("---")

    for issue_def in issues_in_file:
        repo_name = issue_def.get('repo')
        title = issue_def.get('title')
        
        if not all([repo_name, title]):
            print("WARNING: Skipped an issue because it is missing the 'repo' or 'title' field in the YAML.")
            continue

        full_repo_path = f"{GITHUB_ORG}/{repo_name}"
        api_url = f'https://api.github.com/repos/{full_repo_path}/issues'
        
        # Build the issue body, adding the suggested branch if it exists.
        body = issue_def.get('body', '')
        branch_name = issue_def.get('branch')
        if branch_name:
            body += f"\n\n---\n**Suggested Branch:**\n```\n{branch_name}\n```"

        issue_payload = {
            'title': title,
            'body': body,
            'labels': issue_def.get('labels', [])
        }

        print(f"Creating issue '{title}' in repository '{full_repo_path}'...")
        
        response = requests.post(api_url, headers=headers, json=issue_payload)

        if response.status_code == 201:
            issue_url = response.json().get('html_url')
            print(f"  ✅ Success! Issue created at: {issue_url}")
        else:
            print(f"  ❌ Error! Could not create issue. Status code: {response.status_code}")
            print(f"     API response: {response.text}")
        
        print("---")

    print("\nIssue creation process completed.")


if __name__ == "__main__":
    # The GitHub Actions workflow passes the file path as an argument.
    # sys.argv[0] is the script name, sys.argv[1] is the first argument.
    if len(sys.argv) > 1:
        # Use the path provided by the workflow.
        file_to_process = sys.argv[1]
    else:
        # If run manually without arguments, use a default value.
        print("WARNING: No path provided as argument. Using 'sprint_setup.yml' by default.")
        file_to_process = 'sprint_setup.yml'
    
    create_sprint_issues(file_to_process)