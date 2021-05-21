import time

from jira import JIRA
import os


class JiraConnector:
    def __init__(self):
        self.user = os.environ.get('JIRA_BOT_USERNAME')
        self.password = os.environ.get('JIRA_BOT_PASSWORD')
        self.jira_session = JIRA(server="YOUR SERVER URL", basic_auth=(self.user, self.password))
        self.board_id = 148

    @staticmethod
    def build_ticket(browser, version):

        return {
               "project":
               {
                  "key": "ASS"
               },
               "summary": "SMOKE: {} released a new version {}".format(browser, version),
               "description": "Smoke check main functionality of {}".format(browser),
               "priority": {"name": "Major"},
               "customfield_11800": {"value": "RnD"},
               "timetracking": {"originalEstimate": "1h"},
               "issuetype": {
                  "name": "Testing"
               },

           }

    def create_issue(self, browser, version):
        issue = self.build_ticket(browser, version)
        new_issue = self.jira_session.create_issue(fields=issue)

        return new_issue

    #TODO figure out how to choose active sprint in different way
    def get_active_sprint_id(self):
        "Some magic in choosing sprint"
        sprints = self.jira_session.sprints(board_id=self.board_id)
        position = len(sprints)-3
        print(sprints[position].name)

        if 'RnD' in sprints[position].name:
            sprint_id = sprints[position].id
        elif 'RnD' in sprints[position-1].name:
            sprint_id = sprints[position - 1].id
        else:
            sprint_id = sprints[position - 2].id

        print(sprint_id)

        return int(sprint_id)

    def add_issue_to_active_sprint(self, issue_key):
        self.jira_session.add_issues_to_sprint(self.get_active_sprint_id(), [issue_key])

    def create_issue_for_testing(self, browser, version):
        issue_key = self.create_issue(browser, version)
        self.add_issue_to_active_sprint(str(issue_key))
        time.sleep(5)
        issue_key.update(fields={"labels": ["smoke", "rnd_internal", "planned"]})