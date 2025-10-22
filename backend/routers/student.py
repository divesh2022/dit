from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.services.auth import AuthService
from backend.database import get_db
from backend.shared.utils import parse_bearer_token, token_has_role

router = APIRouter(prefix="/student", tags=["Student"])


class StudentReport(BaseModel):
    student_id: int
    subject_code: Optional[str] = None
    subject_name: Optional[str] = None
    marks: Optional[float] = None
    grade: Optional[str] = None
    semester: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True
        extra = "allow"


def get_current_student(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    Decode JWT, ensure role is 'student', and return at least {'id', 'username'}.
    Expects token to include 'sub' or 'user_id' or 'id' with the student's id.
    """
    token = parse_bearer_token(authorization)
    payload = AuthService.decode_token(token)

    if not token_has_role(payload, "student"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized as student")

    student_id = payload.get("sub") or payload.get("user_id") or payload.get("id")
    if not student_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token missing student id")

    return {"id": int(student_id), "username": payload.get("username")}


@router.get("/me")
def read_me(current_student: Dict[str, Any] = Depends(get_current_student)):
    """Return minimal profile for authenticated student"""
    return {"id": current_student["id"], "username": current_student.get("username")}


@router.get("/reports", response_model=List[StudentReport])
def get_my_reports(
    subject_code: Optional[str] = None,
    semester: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    current_student: Dict[str, Any] = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """
    Query the view `student_report_view` for records belonging to the current student.
    Optional filters: subject_code, semester. Pagination via limit/offset.
    """
    sql = "SELECT * FROM student_report_view WHERE student_id = :student_id"
    params = {"student_id": current_student["id"]}

    if subject_code:
        sql += " AND subject_code = :subject_code"
        params["subject_code"] = subject_code

    if semester:
        sql += " AND semester = :semester"
        params["semester"] = semester

    sql += " ORDER BY subject_code NULLS LAST LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    try:
        result = db.execute(text(sql), params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB query failed: {e}")

    rows = result.mappings().all()
    reports = []
    for r in rows:
        row = dict(r)
        extra = {k: v for k, v in row.items() if k not in (
            "student_id", "subject_code", "subject_name", "marks", "grade", "semester"
        )}
        reports.append(
            StudentReport(
                student_id=row.get("student_id"),
                subject_code=row.get("subject_code"),
                subject_name=row.get("subject_name"),
                marks=row.get("marks"),
                grade=row.get("grade"),
                semester=row.get("semester"),
                extra=extra or None,
            )
        )
    return reports


@router.get("/reports/{subject_code}", response_model=StudentReport)
def get_report_by_subject(
    subject_code: str,
    current_student: Dict[str, Any] = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """
    Return a single report record for the current student and given subject_code.
    """
    sql = """
        SELECT * FROM student_report_view
        WHERE student_id = :student_id AND subject_code = :subject_code
        LIMIT 1
    """
    params = {"student_id": current_student["id"], "subject_code": subject_code}

    try:
        result = db.execute(text(sql), params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB query failed: {e}")

    row = result.mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Report not found")

    row = dict(row)
    extra = {k: v for k, v in row.items() if k not in (
        "student_id", "subject_code", "subject_name", "marks", "grade", "semester"
    )}

    return StudentReport(
        student_id=row.get("student_id"),
        subject_code=row.get("subject_code"),
        subject_name=row.get("subject_name"),
        marks=row.get("marks"),
        grade=row.get("grade"),
        semester=row.get("semester"),
        extra=extra or None,
    )