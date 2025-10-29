-- Branch Table
CREATE TABLE Branch (
    branch_id INT PRIMARY KEY IDENTITY(1,1),
    branch_name NVARCHAR(100) NOT NULL
);

-- Role Table
CREATE TABLE Role (
    role_id CHAR(5) PRIMARY KEY,
    role_name NVARCHAR(50) NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    password NVARCHAR(100) NOT NULL
);

-- StudentDetails Table
CREATE TABLE StudentDetails (
    student_id INT PRIMARY KEY IDENTITY(1000,1),
    student_name NVARCHAR(100),
    father_name NVARCHAR(100),
    branch_id INT,
    college_name NVARCHAR(100),
    gender NVARCHAR(6) CHECK (gender IN ('Male', 'Female')),
    dob DATE,
    category NVARCHAR(50),
    sub_category NVARCHAR(50)
);

-- FacultyDetails Table
CREATE TABLE FacultyDetails (
    faculty_id INT PRIMARY KEY IDENTITY(500,1),
    faculty_name NVARCHAR(100),
    designation NVARCHAR(50),
    department NVARCHAR(50),
    email NVARCHAR(100),
    phone NVARCHAR(15)
);

-- Course Table
CREATE TABLE Course (
    subject_code VARCHAR(10) PRIMARY KEY,
    subject_name NVARCHAR(100),
    syllabus_path NVARCHAR(MAX),
    branch_id INT,
    credits INT
);

-- StudentAcademic Table
CREATE TABLE StudentAcademic (
    student_id INT PRIMARY KEY,
    current_sem INT,
    grade CHAR(2),
    cgpa DECIMAL(4,2),
    status BIT, -- 0: Inactive, 1: Active
    branch_id INT,
    FOREIGN KEY (student_id) REFERENCES StudentDetails(student_id),
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);

-- FacultyTeaching Table
CREATE TABLE FacultyTeaching (
    faculty_id INT,
    subject_code VARCHAR(10),
    sem_taught INT,
    PRIMARY KEY (faculty_id, subject_code),
    FOREIGN KEY (faculty_id) REFERENCES FacultyDetails(faculty_id),
    FOREIGN KEY (subject_code) REFERENCES Course(subject_code)
);

-- Exam Table
CREATE TABLE Exam (
    exam_id INT PRIMARY KEY IDENTITY(1,1),
    question_paper_path NVARCHAR(MAX),
    exam_date DATE,
    subject_code VARCHAR(10),
    faculty_id INT,
    total_marks INT,
    FOREIGN KEY (subject_code) REFERENCES Course(subject_code),
    FOREIGN KEY (faculty_id) REFERENCES FacultyDetails(faculty_id)
);

-- Marks Table
CREATE TABLE Marks (
    student_id INT,
    exam_id INT,
    marks_obtained INT,
    grade CHAR(2),
    response_sheet_path NVARCHAR(MAX),
    PRIMARY KEY (student_id, exam_id),
    FOREIGN KEY (student_id) REFERENCES StudentDetails(student_id),
    FOREIGN KEY (exam_id) REFERENCES Exam(exam_id)
);

-- Assignment Table
CREATE TABLE Assignment (
    assignment_id INT PRIMARY KEY IDENTITY(1,1),
    faculty_id INT,
    question_paper NVARCHAR(MAX),
    date_of_creation DATE,
    date_of_submission DATE,
    total_marks INT,
    branch_id INT,
    FOREIGN KEY (faculty_id) REFERENCES FacultyDetails(faculty_id),
    FOREIGN KEY (branch_id) REFERENCES Branch(branch_id)
);

-- AssignmentMarks Table
CREATE TABLE AssignmentMarks (
    student_id INT,
    assignment_id INT,
    marks_obtained INT,
    grade CHAR(2),
    status INT CHECK (status IN (0, 1)), -- 0: One-time, 1: Late
    PRIMARY KEY (student_id, assignment_id),
    FOREIGN KEY (student_id) REFERENCES StudentDetails(student_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignment(assignment_id)
);

-- Attendance Table
CREATE TABLE Attendance (
    student_id INT,
    subject_code VARCHAR(10),
    faculty_id INT,
    current_attendance INT,
    PRIMARY KEY (student_id, subject_code, faculty_id),
    FOREIGN KEY (student_id) REFERENCES StudentDetails(student_id),
    FOREIGN KEY (subject_code) REFERENCES Course(subject_code),
    FOREIGN KEY (faculty_id) REFERENCES FacultyDetails(faculty_id)
);