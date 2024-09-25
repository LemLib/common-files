#!/usr/bin/env python3

from git import Repo
from pathlib import Path
from os import path, environ, makedirs, EX_OK, EX_CANTCREAT
from sys import stderr, stdin, stdout
import subprocess
from github import Github, Auth, GithubException, Repository
import tomllib
from time import sleep

def get_git_url(repo_name : str) -> str:
    username = "leminator3000"
    return f"https://{environ["secrets.pat"]}@github.com/{username}/{repo_name}.git/"

toml_file = Path("common-files/files.toml").open()

if path.isdir("__repos__") or  path.isfile("__repos__"):
    print("__repos__ should not already exist in the repo!", file=stderr)
    exit(EX_CANTCREAT)
else:
    makedirs("__repos__")
subprocess.run("cd __repos__",check=True,shell=True)
#print(Path.cwd())
#exit(EX_OK)

github_user = Github(auth=Auth.Token(environ["secrets.pat"])).get_user()
for repo in Github.search_repositories(github_user, "org:Lemlib "):
    fork : Repository.Repository = None
    try:
        fork = github_user.get_repo(repo.name)
    except GithubException:
        fork = github_user.create_fork(repo)
        fork.rename_branch("main", "maintenance")
        sleep(5) # allow time for github to update since it seems like rename_branch doesn't block
        subprocess.run(["git", "clone", fork.git_url],check=True)
    subprocess.run(["git", "remote", "add", "upstream", repo.git_url],check=True)