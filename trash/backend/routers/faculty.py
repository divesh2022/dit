from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime

from backend.services.auth import AuthService
from backend.database import get_db
from backend.shared.utils import parse_bearer_token

router = APIRouter(prefix="/faculty", tags=["Faculty"])


class FacultyProfile(BaseModel):
    id: int
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None


class StudentOut(BaseModel):
    id: int
    username: Optional[str] = None
    full_name: Optional[str] = None
    roll_no: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True


class CourseOut(BaseModel):
    id: int
    subject_code: Optional[str] = None
    subject_name: Optional[str] = None
    semester: Optional[str] = None

    class Config:
        orm_mode = True


class AssignmentIn(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    course_id: int


class AssignmentOut(AssignmentIn):
    id: int
    faculty_id: int

    class Config:
        orm_mode = True


def get_current_faculty(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    token = parse_bearer_token(authorization)
    try:
        payload = AuthService.decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    role = payload.get("role") or payload.get("roles")
    if isinstance(role, list):
        allowed = "faculty" in role or any(str(r).lower() == "faculty" for r in role)
    else:
        allowed = role and str(role).lower() == "faculty"

    if not allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized as faculty")

    faculty_id = payload.get("sub") or payload.get("user_id") or payload.get("id")
    if not faculty_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token does not contain faculty id")

    return {"id": int(faculty_id), "username": payload.get("username"), "email": payload.get("email")}


@router.get("/me", response_model=FacultyProfile)
def read_me(current_faculty: Dict[str, Any] = Depends(get_current_faculty)):
    return FacultyProfile(id=current_faculty["id"], username=current_faculty.get("username"),
                          email=current_faculty.get("email"))


@router.get("/students", response_model=List[StudentOut])
def get_assigned_students(
    limit: int = 100,
    offset: int = 0,
    current_faculty: Dict[str, Any] = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    """
    Return students assigned to the current faculty (students.faculty_id = current_faculty.id).
    """
    sql = """
        SELECT id, username, full_name, roll_no, email
        FROM students
        WHERE faculty_id = :faculty_id
        ORDER BY id
        LIMIT :limit OFFSET :offset
    """
    params = {"faculty_id": current_faculty["id"], "limit": limit, "offset": offset}
    try:
        result = db.execute(text(sql), params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB query failed: {e}")

    rows = result.mappings().all()
    return [StudentOut(**dict(r)) for r in rows]


@router.get("/courses", response_model=List[CourseOut])
def get_faculty_courses(
    current_faculty: Dict[str, Any] = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    """
    Return courses where courses.faculty_id = current_faculty.id
    """
    sql = """
        SELECT id, subject_code, subject_name, semester
        FROM courses
        WHERE faculty_id = :faculty_id
        ORDER BY subject_code
    """
    params = {"faculty_id": current_faculty["id"]}
    try:
        result = db.execute(text(sql), params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB query failed: {e}")

    rows = result.mappings().all()
    return [CourseOut(**dict(r)) for r in rows]


@router.post("/assignments", response_model=AssignmentOut, status_code=status.HTTP_201_CREATED)
def create_assignment(
    payload: AssignmentIn,
    current_faculty: Dict[str, Any] = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    """
    Create assignment for a course only if the current faculty teaches that course.
    """
    # verify faculty teaches course
    check_sql = "SELECT id FROM courses WHERE id = :course_id AND faculty_id = :faculty_id LIMIT 1"
    try:
        found = db.execute(text(check_sql), {"course_id": payload.course_id, "faculty_id": current_faculty["id"]}).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB query failed: {e}")

    if not found:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create assignment for this course")

    insert_sql = """
        INSERT INTO assignments (title, description, due_date, course_id, faculty_id, created_at)
        VALUES (:title, :description, :due_date, :course_id, :faculty_id, now())
        RETURNING id, title, description, due_date, course_id, faculty_id
    """
    params = {
        "title": payload.title,
        "description": payload.description,
        "due_date": payload.due_date,
        "course_id": payload.course_id,
        "faculty_id": current_faculty["id"],
    }
    try:
        result = db.execute(text(insert_sql), params)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create assignment: {e}")

    row = result.mappings().first()
    return AssignmentOut(**dict(row))


@router.put("/assignments/{assignment_id}", response_model=AssignmentOut)
def update_assignment(
    assignment_id: int,
    payload: AssignmentIn,
    current_faculty: Dict[str, Any] = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    """
    Update assignment only if it belongs to the current faculty.
    """
    # ensure assignment exists and belongs to faculty
    check_sql = "SELECT id FROM assignments WHERE id = :id AND faculty_id = :faculty_id LIMIT 1"
    try:
        found = db.execute(text(check_sql), {"id": assignment_id, "faculty_id": current_faculty["id"]}).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB query failed: {e}")

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found or not authorized")

    update_sql = """
        UPDATE assignments
        SET title = :title, description = :description, due_date = :due_date, course_id = :course_id, updated_at = now()
        WHERE id = :id
        RETURNING id, title, description, due_date, course_id, faculty_id
    """
    params = {
        "id": assignment_id,
        "title": payload.title,
        "description": payload.description,
        "due_date": payload.due_date,
        "course_id": payload.course_id,
    }
    try:
        result = db.execute(text(update_sql), params)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update assignment: {e}")

    row = result.mappings().first()
    return AssignmentOut(**dict(row))


@router.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(
    assignment_id: int,
    current_faculty: Dict[str, Any] = Depends(get_current_faculty),
    db: Session = Depends(get_db),
):
    """
    Delete assignment only if it belongs to the current faculty.
    """
    check_sql = "SELECT id FROM assignments WHERE id = :id AND faculty_id = :faculty_id LIMIT 1"
    try:
        found = db.execute(text(check_sql), {"id": assignment_id, "faculty_id": current_faculty["id"]}).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB query failed: {e}")

    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found or not authorized")

    delete_sql = "DELETE FROM assignments WHERE id = :id"
    try:
        db.execute(text(delete_sql), {"id": assignment_id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete assignment: {e}")

    return None