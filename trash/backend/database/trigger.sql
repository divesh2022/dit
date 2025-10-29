USE stud_man;
GO

-- 🔁 Trigger: Auto-create StudentAcademic record when a new student is added
CREATE TRIGGER trg_SetStudentStatus
ON StudentDetails
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO StudentAcademic (student_id, current_sem, grade, cgpa, status, branch_id)
    SELECT 
        i.student_id,
        1,             -- Default semester
        'NA',          -- Default grade
        0.0,           -- Default CGPA
        1,             -- Active status
        i.branch_id
    FROM inserted i;
END;
GO

-- 📉 Trigger: Prevent deletion of a Course if referenced in Exam or FacultyTeaching
CREATE TRIGGER trg_PreventCourseDelete
ON Course
INSTEAD OF DELETE
AS
BEGIN
    IF EXISTS (
        SELECT 1 FROM Exam WHERE subject_code IN (SELECT subject_code FROM deleted)
        UNION
        SELECT 1 FROM FacultyTeaching WHERE subject_code IN (SELECT subject_code FROM deleted)
    )
    BEGIN
        RAISERROR ('Cannot delete course: referenced in Exam or FacultyTeaching.', 16, 1);
        RETURN;
    END

    DELETE FROM Course WHERE subject_code IN (SELECT subject_code FROM deleted);
END;
GO

-- 📝 Trigger: Log assignment submissions in AssignmentAudit
CREATE TRIGGER trg_LogAssignmentSubmission
ON AssignmentMarks
AFTER INSERT
AS
BEGIN
    INSERT INTO AssignmentAudit (student_id, assignment_id)
    SELECT student_id, assignment_id FROM inserted;
END;
GO

-- 📊 Trigger: Update CGPA in StudentAcademic when new marks are inserted
CREATE TRIGGER trg_UpdateCGPA
ON Marks
AFTER INSERT
AS
BEGIN
    UPDATE sa
    SET cgpa = (
        SELECT AVG(CAST(marks_obtained AS FLOAT)) / 10
        FROM Marks m
        WHERE m.student_id = sa.student_id
    )
    FROM StudentAcademic sa
    INNER JOIN inserted i ON sa.student_id = i.student_id;
END;
GO

-- 🚫 Trigger: Prevent duplicate attendance entries
CREATE TRIGGER trg_PreventDuplicateAttendance
ON Attendance
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Attendance a
        JOIN inserted i ON a.student_id = i.student_id AND a.subject_code = i.subject_code AND a.faculty_id = i.faculty_id
    )
    BEGIN
        RAISERROR ('Duplicate attendance entry detected.', 16, 1);
        RETURN;
    END

    INSERT INTO Attendance (student_id, subject_code, faculty_id, current_attendance)
    SELECT student_id, subject_code, faculty_id, current_attendance FROM inserted;
END;
GO