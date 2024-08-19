import os
import re
import json
import sys
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

INTERNAL_404_URL = "https://github.com/sei-protocol/sei-docs/blob/main/pages/404.mdx"
MAX_WORKERS = 5

def check_url_status(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code, response.reason, response.url
    except requests.RequestException as e:
        return None, str(e), None

def find_urls(text):
    url_pattern = re.compile(r'https?://[^\s"\'<>\)]*')
    return url_pattern.findall(text)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def process_file(file_path):
    file_report = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                urls = find_urls(line)
                for url in urls:
                    if is_valid_url(url):
                        status_code, reason, final_url = check_url_status(url)
                        if status_code and status_code not in {200, 403, 415, 501} and final_url != INTERNAL_404_URL:
                            file_report.append({
                                'file': file_path,
                                'line': line_number,
                                'url': url,
                                'status_code': status_code,
                                'reason': reason,
                                'final_url': final_url
                            })
    except IOError as e:
        print(f"Error reading file {file_path}: {str(e)}")
    return file_report

def check_location(location):
    all_reports = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_file = {}
        if os.path.isfile(location):
            future = executor.submit(process_file, location)
            future_to_file[future] = location
        else:
            for root, _, files in os.walk(location):
                for file in files:
                    if file.endswith(('.md', '.mdx')):
                        file_path = os.path.join(root, file)
                        future = executor.submit(process_file, file_path)
                        future_to_file[future] = file_path

        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                report = future.result()
                all_reports.extend(report)
            except Exception as exc:
                print(f'{file_path} generated an exception: {exc}')

    return all_reports

def generate_report(report):
    output = {
        "total_issues": len(report),
        "issues": report
    }
    return json.dumps(output)

if __name__ == "__main__":
    check_path = os.environ.get('CHECK_PATH', './pages/')
    print(f"Checking URLs in location: {check_path}", file=sys.stderr)
    report = check_location(check_path)
    output = generate_report(report)
    print(output)
