from pathlib import Path
import git
from datetime import datetime
from typing import List, Optional
from ..models.commit import Commit
from ..models.file import File

class RepoManager:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.repo = git.Repo(repo_path)

    def init_repo(self) -> bool:
        """Initialize a new git repository"""
        try:
            if not self.repo_path.exists():
                git.Repo.init(self.repo_path)
            return True
        except git.GitCommandError as e:
            print(f"Error initializing repo: {e}")
            return False

    def get_commit_history(self) -> List[Commit]:
        """Get repository commit history"""
        commits = []
        for commit in self.repo.iter_commits():
            commits.append(Commit(
                hash=commit.hexsha,
                author=commit.author.name,
                message=commit.message,
                date=datetime.fromtimestamp(commit.committed_date)
            ))
        return commits

    def get_changed_files(self) -> List[File]:
        """Get list of modified files"""
        changed_files = []
        diff = self.repo.index.diff(None)
        for item in diff:
            changed_files.append(File(
                path=item.a_path,
                status=item.change_type,
                last_modified=datetime.now()
            ))
        return changed_files

    def commit_changes(self, message: str, author: str) -> Optional[str]:
        """Commit changes to repository"""
        try:
            self.repo.index.add('*')
            commit = self.repo.index.commit(message)
            return commit.hexsha
        except git.GitCommandError as e:
            print(f"Error committing changes: {e}")
            return None