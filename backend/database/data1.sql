use stud_man;
-- Branch
INSERT INTO Branch (branch_name) VALUES 
('Computer Science'), 
('Mechanical Engineering'), 
('Electrical Engineering');

-- Role
INSERT INTO Role (role_id, role_name, email, password) VALUES 
('R001', 'Admin', 'admin@college.edu', 'admin123'),
('R002', 'Faculty', 'faculty@college.edu', 'fac123'),
('R003', 'Student', 'student@college.edu', 'stud123');

-- StudentDetails
INSERT INTO StudentDetails (student_name, father_name, branch_id, college_name, gender, dob, category, sub_category) VALUES 
('Amit Sharma', 'Rajesh Sharma', 1, 'Tech Institute', 'Male', '2002-05-15', 'General', 'None'),
('Priya Verma', 'Suresh Verma', 2, 'Tech Institute', 'Female', '2003-08-22', 'OBC', 'None');

-- FacultyDetails
INSERT INTO FacultyDetails (faculty_name, designation, department, email, phone) VALUES 
('Dr. Neha Singh', 'Professor', 'Computer Science', 'neha@college.edu', '9876543210'),
('Mr. Rakesh Kumar', 'Lecturer', 'Mechanical Engineering', 'rakesh@college.edu', '9123456789');

-- Course
INSERT INTO Course (subject_code, subject_name, syllabus_path, branch_id, credits) VALUES 
('CS101', 'Data Structures', 'syllabus/cs101.pdf', 1, 4),  -- Assuming branch_id 1 corresponds to 'Computer Science'
('ME201', 'Thermodynamics', 'syllabus/me201.pdf', 2, 3);  -- Assuming branch_id 2 corresponds to 'Mechanical Engineering'

-- StudentAcademic
INSERT INTO StudentAcademic (student_id, current_sem, grade, cgpa, status, branch_id) VALUES 
(1000, 3, 'B+', 7.8, 1, 1),
(1001, 2, 'A', 8.5, 1, 2);

-- FacultyTeaching
INSERT INTO FacultyTeaching (faculty_id, subject_code, sem_taught) VALUES 
(500, 'CS101', 3),
(501, 'ME201', 2);

-- Exam
INSERT INTO Exam (question_paper_path, exam_date, subject_code, faculty_id, total_marks) VALUES 
('exams/cs101_qp.pdf', '2025-10-10', 'CS101', 500, 100),
('exams/me201_qp.pdf', '2025-10-12', 'ME201', 501, 100);

-- Marks
INSERT INTO Marks (student_id, exam_id, marks_obtained, grade, response_sheet_path) VALUES 
(1000, 1, 78, 'B+', 'responses/1000_cs101.pdf'),
(1001, 2, 85, 'A', NULL);

-- Assignment
INSERT INTO Assignment (faculty_id, question_paper, date_of_creation, date_of_submission, total_marks, branch_id) VALUES 
(500, 'Explain linked list operations', '2025-09-01', '2025-09-10', 20, 1),
(501, 'Describe heat transfer methods', '2025-09-05', '2025-09-15', 25, 2);

-- AssignmentMarks
INSERT INTO AssignmentMarks (student_id, assignment_id, marks_obtained, grade, status) VALUES 
(1000, 1, 18, 'A', 0),
(1001, 2, 22, 'A', 1);

-- Attendance
INSERT INTO Attendance (student_id, subject_code, faculty_id, current_attendance) VALUES 
(1000, 'CS101', 500, 85),
(1001, 'ME201', 501, 90);