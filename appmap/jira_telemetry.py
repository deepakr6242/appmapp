from jira import JIRA
from datetime import datetime
import csv

project_list = []

def authentication():
    user = 'venkatesh_katpally@mednax.com'
    apikey = 'e4Jnah3QYjHEWYa2xRLp9FFA'
    server = 'https://mednax1500.atlassian.net'
    options = {'server': server}
    jira = JIRA(options, basic_auth=(user, apikey))
    return jira

def projects(jira):
    total_projects = jira.projects()
    for i in range(len(total_projects)):
        j = str(total_projects[i])
        project_list.append(j)
        project_list.sort()
    print (project_list)

def which_jql(project_name):
    if project_name == "CHGCAP" or project_name == "NETIQ":
        return "project = " + project_name + " AND status = Production"
    else:
        return "project = " + project_name + " AND status = Done"

def append_in_csv(project_name, task_type_2, fix_version, issue_id, issue_name, in_production_datetime, dev_in_progress_datetime, number_of_days_taken, writer):
    csv_column = []
    csv_column.append(project_name)
    csv_column.append(task_type_2)
    csv_column.append(fix_version.decode("ASCII"))
    csv_column.append(issue_id)
    csv_column.append(issue_name.decode("ASCII"))
    csv_column.append(in_production_datetime)
    #csv_column.append(dev_in_progress_datetime)
    #csv_column.append(in_production_datetime-dev_in_progress_datetime)
    csv_column.append(number_of_days_taken)
    writer.writerow(csv_column)

def release_name(issue_object):
    if len(issue_object.fields.fixVersions) == 0:
        fix_version = "None"
    else:
        fix_version = str(issue_object.fields.fixVersions[0])
    return fix_version.encode("ascii", "ignore")

def days(total_time_taken):
    number_of_days_taken = ""
    number_of_hours_taken = ""
    if total_time_taken.find("days") == 3 or total_time_taken.find("days") == 4 or total_time_taken.find("days") == 2:
        number_of_days_taken = total_time_taken.split(",")[0].split(" ")[0]
        print (number_of_days_taken)
        number_of_hours_taken = total_time_taken.split(",")[1].split(":")[0]
        print (number_of_hours_taken.lstrip())
        if int(number_of_hours_taken.lstrip()) > 12:
            number_of_days_taken = int(number_of_days_taken) + 1
        print (number_of_days_taken)
    else:
        number_of_days_taken = 1
        print (number_of_days_taken)
    return number_of_days_taken

def prod_status_change_history(status_change_history):
    j = ""
    in_production_changelog = ""
    for j in status_change_history:
        #print (j)
        if j.find("From:Production To:Done") != -1 or j.find("From:READY FOR PROD To:Done") != -1 or j.find("From:READY FOR PROD To:Production") != -1 or j.find("From:READY FOR PC To:Deployed") != -1 or j.find("From:Done To:Production") != -1 or j.find("From:IN UAT To:Production") != -1:
            in_production_changelog = j
            break
    return in_production_changelog

def dev_status_change_history(status_change_history):
    qq = ""
    dev_in_progress_changelog = ""
    for qq in reversed(status_change_history):
        #print (qq)
        if qq.find("To:Dev In Progress") != -1:
            dev_in_progress_changelog = qq
            break
        else:
            dev_in_progress_changelog = status_change_history[len(status_change_history)-1]
    return dev_in_progress_changelog

def calculate_final_time_append_in_csv(p, c, issue_list, i, project_name, jira, writer):
    total_time_taken = ""
    task_type = ""
    issue_id = ""
    issue_name = ""
    in_production_datetime = ""
    dev_in_progress_datetime = ""
    #print (issue_list)
    if p.find("From:Production To:Done") != -1 or p.find("From:READY FOR PROD To:Done") != -1 or p.find("From:READY FOR PROD To:Production") != -1 or p.find("From:READY FOR PC To:Deployed") != -1 or p.find("From:Done To:Production") != -1 or p.find("From:IN UAT To:Production") != -1:
        in_production_changelog = p.split('.')[0].split('Date:')[1]
        in_production_datetime = datetime.strptime(in_production_changelog.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        #print (in_production_datetime)
        dev_in_progress_changelog = c.split('.')[0].split('Date:')[1]
        dev_in_progress_datetime = datetime.strptime(dev_in_progress_changelog.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        #print (dev_in_progress_datetime)
        #print (issue_list)
        #print (issue_list[i]["key"])
        issue_id = jira.issue(issue_list[i]["key"])
        issue_object = jira.issue(issue_id)
        task_type = str(issue_object.fields.issuetype).encode("ascii", "ignore")
        task_type_2 = task_type.decode("ASCII")
        fix_version = release_name(issue_object)
        issue_name = str(issue_object.fields.summary).encode("ascii", "ignore")
        total_time_taken = str(in_production_datetime-dev_in_progress_datetime)
        print (total_time_taken)
        #print (total_time_taken.find("days"))
        number_of_days_taken = days(total_time_taken)
        append_in_csv(project_name, task_type_2, fix_version, issue_id, issue_name, in_production_datetime, dev_in_progress_datetime, number_of_days_taken, writer)
        status_change_history = []
        #print (csv_column)
    else:
        status_change_history = []
        #print (status_change_history)

def finding_status_change_history(issue_list, project_name, jira, writer):
    i = ""
    status_change_history = []
    #print (len(issue_list))
    for i in range(len(issue_list)):
        print (issue_list[i]["key"])
        #print (jira.issue(issue_list[i]["key"]))
        issue = jira.issue(issue_list[i]["key"], expand ='changelog')
        changelog = issue.changelog
        for history in changelog.histories:
            for item in history.items:
                if item.field == 'status':
                    result = 'Date:' + history.created + ' From:' + item.fromString + ' To:' + item.toString
                    status_change_history.append(result)
        #print (len(issue_list))
        print (status_change_history)
        p = prod_status_change_history(status_change_history)
        print (p)
        c= dev_status_change_history(status_change_history)
        print (c)
        #print (len(issue_list))
        #print (issue_list[i]["key"])
        calculate_final_time_append_in_csv(p, c, issue_list, i, project_name, jira, writer)
        status_change_history = []

def main():
    jira = authentication()

    csv_file = open("jira_report.csv", "w")
    writer = csv.writer(csv_file)
    header = ["Project Name", "Task Type", "Fix Version", "Task No", "Task Name", "Deployed to Production", "Days"]
    writer.writerow(header)

    projects(jira)

    for pr in range(len(project_list)):
        project_name = ""
        project = project_list[pr]
        project_name = project_list[pr]
        print (project_name)
        jql_query = which_jql(project_name)
        print (jql_query)
        total_numbers_issues = jira.search_issues(jql_str=jql_query, json_result=True)
        if  total_numbers_issues["total"] > 1:
            for startIndex in range(0, total_numbers_issues["total"], 100):
                #print (startIndex)
                query2 = jira.search_issues(jql_query, json_result=True, startAt=startIndex, maxResults=100)
                issue_list = query2["issues"]
                #print (len(issue_list))
                finding_status_change_history(issue_list, project_name, jira, writer)

    csv_file.close()

if __name__ == "__main__":
    main()
