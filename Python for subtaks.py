import requests
import base64


def get_auth_headers(username, api_token):
    return {
        "Authorization": f"Basic {base64.b64encode(f'{username}:{api_token}'.encode('utf-8')).decode('utf-8')}",
        "Content-Type": "application/json"
    }


def find_issues(api_url, username, api_token, jql_query):
    headers = get_auth_headers(username, api_token)
    params = {"jql": jql_query, "maxResults": 1000}  # Adjust maxResults based on your needs
    response = requests.get(f"{api_url}/search", headers=headers, params=params)

    if response.status_code == 200:
        return response.json()["issues"]
    else:
        print(f"Failed to execute JQL query. Status code: {response.status_code}")
        return []


def find_parent_epic(api_url, username, api_token, parent_issue_key):
    headers = get_auth_headers(username, api_token)

    # Get the parent issue details
    response = requests.get(f"{api_url}/issue/{parent_issue_key}", headers=headers)

    if response.status_code == 200:
        parent_issue = response.json()

        # Attempt to find the Epic link
        for link in parent_issue.get("fields", {}).get("issuelinks", []):
            if (
                    link.get("type", {}).get("inward", {}).get("name") == "Epic-Story Link"
                    or link.get("type", {}).get("outward", {}).get("name") == "Epic-Story Link"
                    or link.get("type", {}).get("inward", {}).get("name") == "blocks"
                    or link.get("type", {}).get("outward", {}).get("name") == "blocks"
                    # Add more conditions for other possible link types related to Epics
            ):
                return link.get("outwardIssue", {}).get("key")
    return None


def convert_subtasks(api_url, username, api_token, subtasks, issue_type_to_convert):
    headers = get_auth_headers(username, api_token)

    for subtask in subtasks:
        subtask_key = subtask["key"]

        # Get the parent issue key
        parent_issue_key = subtask.get("fields", {}).get("parent", {}).get("key")

        if parent_issue_key:
            # Get the Epic linked to the parent User Story or Task
            parent_epic_key = find_parent_epic(api_url, username, api_token, parent_issue_key)

            if parent_epic_key:
                # Now you have the key of the Epic linked to the parent User Story or Task
                print(f"The Epic linked to the parent of subtask {subtask_key} is {parent_epic_key}")
            else:
                print(f"No Epic linked to the parent of subtask {subtask_key}")
        else:
            print(f"No parent issue found for subtask {subtask_key}")


if __name__ == "__main__":
    # Jira API details
    jira_url = "https://mysitefortesting.atlassian.net/"
    username = "mani95.upwork@gmail.com"
    api_token = "ATATT3xFfGF0jypNrb6ssL6qX1C_l7aQIWkE_NR2DY90hbsAT6hlRf18xQA_3cijXlNREFo5yu18OF5UeqlwclgBTh7zAOwl5PPVDA-oVBy2T1_lLQTOwAbL8Pb0E0w-6VhLj2VwLyUvFpJSljWytvm8mdYttiCr86AloSnjQRIbCnc0xOluThI=0DE2A671"
    # Issue details
    jql_query = 'issuetype = subtask'  # Customize your JQL query
    issue_type_to_convert = "10005"  # Replace with the ID of the target issue type (e.g., Task)

    # Construct the API URL
    api_url = f"{jira_url}/rest/api/2"

    # Find subtasks using JQL query
    subtasks = find_issues(api_url, username, api_token, jql_query)

    # Convert subtasks and link to the existing Epic
    convert_subtasks(api_url, username, api_token, subtasks, issue_type_to_convert)
