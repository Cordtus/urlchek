
# URL Checker for Documentation

This tool helps you identify broken URLs in your GitHub documentation repository. It automatically scans specified directories and file types, checks the status of the URLs, and creates an issue with the list of broken links.

## Setup Instructions

1. **Clone the Repository**

   Clone your documentation repository and navigate to the repository's root directory.

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Add URL Check Files**

   Place the provided files (`urlcheck.py`, `url_check.yml`, `ISSUE_TEMPLATE_URL_CHECK.md`) in the appropriate directories within your repository:

   - `urlcheck.py` goes into the `scripts/` directory.
   - `url_check.yml` goes into the `.github/workflows/` directory.
   - `ISSUE_TEMPLATE_URL_CHECK.md` is optional and can be used as a template for the generated issues.

3. **Configure the GitHub Action**

   The `url_check.yml` GitHub Action is configured to run daily at midnight. You can adjust the schedule by modifying the `cron` expression:

   ```yaml
   on:
     schedule:
       - cron: '0 0 * * *'  # Modify this for a different schedule
   ```

   You can customize the directory to check, the file types to scan, and the HTTP status codes to ignore by modifying the environment variables in the workflow file:

   ```yaml
   env:
     CHECK_PATH: './pages/'  # Set the directory to scan
     IGNORED_STATUS_CODES: '200,403,405,415,501'  # Set the status codes to ignore
     FILE_EXTENSIONS: '.md,.mdx'  # Set the file types to check
   ```

4. **Run the Workflow**

   Once set up, the workflow will automatically run based on the defined schedule or manually when triggered. It will scan the URLs in your documentation, and if broken links are found, an issue will be created in the repository.

5. **Review and Fix Issues**

   Check the generated issues in your GitHub repository under the "Issues" tab. Each issue will list the broken URLs, their file locations, and the reason for failure.

## Contributing

Feel free to submit pull requests or issues if you find bugs or have suggestions for improvements.
