from jira import JIRA

# Jira server URL
jira_url = "https://mysitefortesting.atlassian.net"

# Jira username and API token
username = "mani95.upwork@gmail.com"
api_token = "ATATT3xFfGF0jypNrb6ssL6qX1C_l7aQIWkE_NR2DY90hbsAT6hlRf18xQA_3cijXlNREFo5yu18OF5UeqlwclgBTh7zAOwl5PPVDA-oVBy2T1_lLQTOwAbL8Pb0E0w-6VhLj2VwLyUvFpJSljWytvm8mdYttiCr86AloSnjQRIbCnc0xOluThI=0DE2A671"

# Create a Jira connection
jira = JIRA(server=jira_url, basic_auth=(username, api_token))

# Define JQL query
jql_query = 'issuetype = subtask'

# Execute JQL query
issues = jira.search_issues(jql_query)

# Loop through subtasks and update issue type and Epic Link
for issue in issues:
    print(f"Issue Key: {issue.key}")

    # Get parent issue details
    parent_issue = jira.issue(issue.fields.parent.key)

    # Check if the parent issue has an epic link field
    if hasattr(parent_issue.fields, 'parent'):
        parent_epic_link = parent_issue.fields.parent
        print(f"Parent Epic Link: {parent_epic_link}")

        # Change issue type from subtask to task
        jira.issue(issue.key).update(fields={'issuetype': {'name': 'Task'}}) # Use the desired issue type name
        # Set Epic Link field
        issue.update(fields={'Parent': parent_epic_link})

        print("Issue type changed to Task, and Epic Link set.")
    else:
        print("Parent issue is not an epic.")

    print("-" * 30)
