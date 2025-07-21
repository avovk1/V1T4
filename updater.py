"""Updater for V1T4 bot, can be used to remotely push update without console"""
from subprocess import Popen
from time import sleep
import git

repo = git.Repo("./")
assert not repo.bare
remote = repo.remotes[0]

def check() -> bool:
    """If the local repo is up to date"""
    return remote.fetch()[0].flags//4 == 1

sleep(10)
repo.remotes[0].pull()

Popen(["python", "main.py"])
print("Update done!")
