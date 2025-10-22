import click
from pathlib import Path
from typing import Optional
from .repo_manager import RepoManager
from .file_tracker import FileTracker
from .plagiarism_checker import PlagiarismChecker

class CLIEngine:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.repo_manager = RepoManager(project_path)
        self.file_tracker = FileTracker(project_path)
        self.plagiarism_checker = PlagiarismChecker()

    def init_project(self) -> bool:
        """Initialize a new project"""
        try:
            self.project_path.mkdir(parents=True, exist_ok=True)
            return self.repo_manager.init_repo()
        except Exception as e:
            print(f"Error initializing project: {e}")
            return False

    def scan_changes(self) -> None:
        """Scan for file changes"""
        changed_files = self.file_tracker.scan_files()
        for file in changed_files:
            if file.status != "unchanged":
                click.echo(f"{file.status}: {file.path}")

    def commit_project(self, message: Optional[str] = None) -> None:
        """Commit changes to repository"""
        if not message:
            message = click.prompt("Enter commit message")
        
        commit_hash = self.repo_manager.commit_changes(
            message=message,
            author="CLI User"
        )
        
        if commit_hash:
            click.echo(f"Changes committed successfully: {commit_hash}")
        else:
            click.echo("Failed to commit changes")

    def check_plagiarism(self) -> None:
        """Check for plagiarism in project files"""
        python_files = list(self.project_path.rglob("*.py"))
        results = self.plagiarism_checker.check_plagiarism(python_files)
        
        if results:
            click.echo("Potential plagiarism detected:")
            for file1, file2, similarity in results:
                click.echo(f"{file1} <-> {file2}: {similarity:.2%} similar")
        else:
            click.echo("No significant code similarities found")