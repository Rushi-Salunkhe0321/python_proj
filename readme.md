
```markdown
# Confluence Dependency Fetcher

This Python script automates the process of extracting dependencies from Confluence pages. It traverses pages to multiple depths, scrapes relevant table data, and generates a CSV report of the dependencies.

---

## Features

- Fetches dependencies from parent and nested Confluence pages (up to 5 depths).
- Extracts table data with specific headers such as **Description**, **Version**, **Importance**, and **Handoff**.
- Automatically appends new pages discovered in the dependencies to the appropriate depth for further scraping.
- Outputs a CSV file (`fetch_dependencies.csv`) containing all the fetched dependencies with detailed metadata.

---

## Prerequisites

1. **Python 3.x**: Ensure you have Python installed. You can download it from [Python.org](https://www.python.org/).
2. **Required Python Libraries**:
   - `BeautifulSoup` (from `bs4`) for HTML parsing.
   - `requests` for HTTP requests.
   - `pandas` for data manipulation.
   - `re` (built-in) for regex operations.

Install required libraries using pip:
```bash
pip install requests beautifulsoup4 pandas
```

3. **Confluence Access Token**:  
   Obtain a Confluence API token to authenticate requests. See [Confluence API Tokens Documentation](https://developer.atlassian.com/cloud/confluence/rest/intro/) for details.

4. **Input File**:  
   A CSV file named `confluence_handoff_pages_last_now_days.csv` with a column named `webui`, containing the initial parent page links.

---

## Usage

1. **Setup the Confluence Token**:
   Replace `Your Confluence Token` in the script with your actual token:
   ```python
   confluence_token = "Your Confluence Token"
   ```

2. **Input File**:
   Ensure the `confluence_handoff_pages_last_now_days.csv` file is in the same directory as the script. This file should contain a column named `webui` with URLs of the Confluence pages to start with.

3. **Run the Script**:
   Execute the script using:
   ```bash
   python fetch_confluence_dependencies.py
   ```

4. **Output**:
   After execution, a file named `fetch_dependencies.csv` will be generated in the same directory. It contains the extracted data with the following columns:
   - `page_title`: Title of the Confluence page.
   - `page_link`: URL of the page.
   - `dependency_no`: Dependency description.
   - `description`: Description of the dependency.
   - `version`: Version details.
   - `importance`: Importance level of the dependency.
   - `notes`: Additional notes.
   - `handoff_link_title`: Title of the handoff link.
   - `handoff_link`: URL of the handoff link.
   - `depth`: Depth of the page (e.g., Parent Page, Depth 1, etc.).

---

## Script Overview

### **Workflow**

1. **Parent Pages**: The script starts with the parent pages provided in the `webui` column of the input CSV.
2. **Depth Levels**: For each page, it:
   - Extracts the title and dependency information.
   - Identifies any linked pages for deeper levels (up to 5 depths).
3. **Data Validation**: Only tables with headers matching `Description`, `Version`, `Importance`, and `Handoff` are processed.
4. **Output**: All data is consolidated into a CSV file.

### **Customization**

- **Depth Limit**: The depth of traversal can be adjusted by modifying the `depth_list`.
- **Headers Filtering**: You can customize the headers to look for in the tables by changing the conditions in:
   ```python
   if any(re.search(r'Description', h) for h in headers) and ...
   ```

---

## Notes

- Ensure you have network access to the Confluence instance when running the script.
- This script is designed for internal use and works with `https://qwiki.intranet.qualys.com` URLs. Adjust the base URL (`qwiki.intranet.qualys.com`) if your Confluence instance is hosted elsewhere.

---

## Example

### Input CSV (`confluence_handoff_pages_last_now_days.csv`):
| webui                                 |
|---------------------------------------|
| /pages/viewpage.action?pageId=1234567 |

### Output CSV (`fetch_dependencies.csv`):
| page_title  | page_link                         | dependency_no | description | version | importance | notes | handoff_link_title | handoff_link             | depth       |
|-------------|-----------------------------------|---------------|-------------|---------|------------|-------|---------------------|--------------------------|-------------|
| ExamplePage | /pages/viewpage.action?pageId=1  | Dep1          | Desc1       | 1.0     | High       | Note1 | LinkTitle1         | /display/HODOC/1234567   | Parent Page |

---

## Troubleshooting

- **Authentication Issues**: Verify your token and ensure you have access to the Confluence instance.
- **Empty Output**: Ensure the input CSV file has valid `webui` links and the target pages contain the expected table structures.
- **Dependencies Not Detected**: Confirm the headers in the Confluence tables match the script's filter criteria.

---

## License

This script is distributed under the MIT License. Feel free to use and modify it according to your needs.

---

## Contribution

Feel free to open issues or contribute enhancements via pull requests.
```

Let me know if you need further customization!