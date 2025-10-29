from typing import List, Tuple
from pathlib import Path
import difflib
import tokenize
from io import BytesIO

class PlagiarismChecker:
    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold

    def tokenize_python_code(self, code: str) -> List[str]:
        """Convert Python code to tokens, ignoring comments and whitespace"""
        tokens = []
        try:
            for tok in tokenize.tokenize(BytesIO(code.encode('utf-8')).readline):
                if tok.type not in [tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE]:
                    tokens.append(tok.string)
        except tokenize.TokenError:
            pass
        return tokens

    def calculate_similarity(self, code1: str, code2: str) -> float:
        """Calculate similarity ratio between two code snippets"""
        tokens1 = self.tokenize_python_code(code1)
        tokens2 = self.tokenize_python_code(code2)
        
        matcher = difflib.SequenceMatcher(None, tokens1, tokens2)
        return matcher.ratio()

    def check_plagiarism(self, files: List[Path]) -> List[Tuple[str, str, float]]:
        """Check for plagiarism between multiple files"""
        results = []
        for i, file1 in enumerate(files):
            for file2 in files[i + 1:]:
                try:
                    with open(file1, 'r') as f1, open(file2, 'r') as f2:
                        code1 = f1.read()
                        code2 = f2.read()
                        
                    similarity = self.calculate_similarity(code1, code2)
                    if similarity >= self.similarity_threshold:
                        results.append((str(file1), str(file2), similarity))
                except Exception as e:
                    print(f"Error comparing {file1} and {file2}: {e}")
                    
        return results