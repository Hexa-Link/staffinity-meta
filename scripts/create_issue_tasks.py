import os
import sys
import yaml
import requests

# The script is now hardcoded to ALWAYS create issues in this specific repository.
TARGET_REPO = 'Hexa-Link/staffinity-meta'

def create_issues_from_file(file_path):
    """
    Reads a YML file and creates the corresponding issues in the TARGET_REPO.
    """
    print(f"Loading tasks from file: '{file_path}'")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"FATAL: File '{file_path}' not found.")
        sys.exit(1)

    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("FATAL: GITHUB_TOKEN environment variable is not set.")
        sys.exit(1)

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    api_url = f'https://api.github.com/repos/{TARGET_REPO}/issues'
    
    # Looks for 'tasks' or 'issues' key in the YML for flexibility
    tasks = data.get('tasks', data.get('issues', []))
    print(f"Found {len(tasks)} tasks to create in repository {TARGET_REPO}.")
    print("---")

    for task in tasks:
        # The only necessary validation now is that the task has a title.
        title = task.get('title')
        if not title:
            print("WARNING: Skipped a task because it lacks the 'title' field in the YML.")
            continue

        payload = {
            'title': title,
            'body': task.get('body', ''),
            'labels': task.get('labels', []),
            'assignees': task.get('assignees', [])
        }

        print(f"\nCreating issue: '{payload['title']}'...")
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 201:
            issue_url = response.json().get('html_url')
            print(f"  ✅ Success! Issue created at: {issue_url}")
        else:
            print(f"  ❌ Error! Code: {response.status_code}")
            print(f"     Response: {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_issue_tasks.py <yml_file_path>")
        sys.exit(1)
    create_issues_from_file(sys.argv[1])