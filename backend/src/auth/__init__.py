from github import Github

# First create a Github instance:
class GitHubAuth:
    def __init__(self, access_token:str):
        self.g = Github(access_token)
        
    def get_user(self):
        return self.g.get_user()
    
    def get_repo(self, repo_name):
        return self.g.get_repo(repo_name)