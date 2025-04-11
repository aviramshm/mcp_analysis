import os
import subprocess
import requests
from bs4 import BeautifulSoup
import json

# Constants
BASE_DIR = 'mcp_scanning'
GITHUB_URL = 'https://github.com/punkpeye/awesome-mcp-servers?tab=readme-ov-file'

def fetch_repos():
    response = requests.get(GITHUB_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract all repository URLs from the page
    repo_links = soup.select('a[href^="https://github.com/"]')
    
    # Filter the list to include only the desired range of repositories
    start_repo = "0xdaef0f/job-searchoor"
    end_repo = "Gaffx/volatility-mcp"
    start_index = None
    end_index = None
    
    # Find the start and end indices
    for i, link in enumerate(repo_links):
        href = link['href'].lower()
        if start_repo.lower() in href:
            start_index = i
        if end_repo.lower() in href:
            end_index = i
            break
    
    # Return the filtered list of repository URLs
    if start_index is not None and end_index is not None:
        return [link['href'] for link in repo_links[start_index:end_index + 1]]
    else:
        print("Start or end repository not found.")
        return []

def clone_or_update_repo(repo_url):
    # Split the URL to extract the repository owner and name
    repo_parts = repo_url.split('/')
    print (repo_url)
    # Find the index of 'github.com' to correctly identify the owner and repo name
    try:
        github_index = repo_parts.index('github.com')
        repo_owner = repo_parts[github_index + 1]
        repo_name = repo_parts[github_index + 2]
    except (ValueError, IndexError):
        print(f"Invalid GitHub URL: {repo_url}")
        return None  # Return None if the URL is invalid

    # Construct the root URL of the repository
    root_repo_url = f"https://github.com/{repo_owner}/{repo_name}"

    repo_path = os.path.join(BASE_DIR, repo_name)
    if os.path.exists(repo_path):
        print(f"Repository {repo_name} already exists. Skipping clone.")
    else:
        print(f"Cloning repository: {repo_name}")
        subprocess.run(['git', 'clone', root_repo_url, repo_path])
    
    return repo_path  # Ensure repo_path is returned

def scan_repo(repo_path):
    repo_name = os.path.basename(repo_path)
    output_file = f"{repo_name}.json"
    print(f"Scanning repository: {repo_name}")
    
    subprocess.run(['gitleaks', 'dir', repo_path, '-f', 'json', '-r', output_file, '-c', './gitleaks.toml'])

def generate_report():
    report = {}
    for repo_name in os.listdir(BASE_DIR):
        json_file = f"{repo_name}.json"
        if os.path.exists(json_file):
            with open(json_file) as f:
                data = json.load(f)
                report[repo_name] = {
                    'number_of_secrets': len(data),
                    'secrets': data
                }
    with open('report.json', 'w') as f:
        json.dump(report, f, indent=4)

def main():
    os.makedirs(BASE_DIR, exist_ok=True)
    repos = fetch_repos()
    
    for repo_url in repos:
        print(f"Working on repository: {repo_url}")
        repo_path = clone_or_update_repo(repo_url)
        if repo_path:  # Check if repo_path is not None
            scan_repo(repo_path)
    
    generate_report()

if __name__ == '__main__':
    main()