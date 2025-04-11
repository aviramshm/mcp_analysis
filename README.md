# MCP Scanning Tool

This project is a tool designed to scan a list of GitHub repositories for secrets using `gitleaks`. It clones the repositories, performs the scan, and generates a report summarizing the findings.

## Features
- Fetches a list of repositories from a specified GitHub page.
- Clones or updates repositories locally.
- Scans repositories for secrets using `gitleaks`.
- Generates a JSON report with the number of secrets and their details.

## Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/aviramshm/mcp_analysis.git
   cd mcp_analysis
   ```

2. **Install Dependencies**
   Ensure you have `gitleaks` installed on your system. You can install it using:
   ```bash
   brew install gitleaks
   ```

3. **Configure the Script**
   - Update the `GITHUB_URL` in `mcp_scan.py` to point to the desired GitHub page.
   - Ensure the `gitleaks.toml` configuration file is present in the project directory.

## Usage

Run the script to start scanning:
```bash
python mcp_scan.py
```

The script will:
- Fetch and clone the specified repositories.
- Scan each repository for secrets.
- Generate a `report.json` file with the scan results.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 
