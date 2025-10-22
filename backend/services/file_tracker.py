from pathlib import Path
from typing import List, Dict
import hashlib
from datetime import datetime
from ..models.file import File

class FileTracker:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.file_hashes: Dict[str, str] = {}

    def get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def scan_files(self) -> List[File]:
        """Scan directory for files and track changes"""
        tracked_files = []
        for file_path in self.base_path.rglob('*'):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(self.base_path))
                current_hash = self.get_file_hash(file_path)
                status = "modified" if rel_path in self.file_hashes and self.file_hashes[rel_path] != current_hash else "unchanged"
                
                tracked_files.append(File(
                    path=rel_path,
                    status=status,
                    last_modified=datetime.fromtimestamp(file_path.stat().st_mtime)
                ))
                
                self.file_hashes[rel_path] = current_hash
                
        return tracked_files

    def get_file_status(self, file_path: str) -> str:
        """Get status of specific file"""
        full_path = self.base_path / file_path
        if not full_path.exists():
            return "deleted"
        
        current_hash = self.get_file_hash(full_path)
        if file_path not in self.file_hashes:
            return "new"
        return "modified" if self.file_hashes[file_path] != current_hash else "unchanged"