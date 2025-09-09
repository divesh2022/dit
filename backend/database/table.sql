use smss;
-- STUDENT
CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    roll_number VARCHAR(20) UNIQUE,
    branch VARCHAR(50),
    semester INT,
    contact_info VARCHAR(100),
    email VARCHAR(100),
    emergency_contact VARCHAR(100)
);

-- FACULTY
CREATE TABLE Faculty (
    faculty_id INT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    office_hours VARCHAR(50),
    contact_info VARCHAR(100)
);

-- FACULTY_DETAILS
CREATE TABLE FacultySubjects (
    faculty_id INT,
    subject VARCHAR(100),
    PRIMARY KEY (faculty_id, subject),
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id)
);

CREATE TABLE FacultyEducation (
    faculty_id INT,
    qualification VARCHAR(200),
    PRIMARY KEY (faculty_id, qualification),
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id)
);

CREATE TABLE FacultyResearchArea (
    faculty_id INT,
    research_area VARCHAR(200),
    PRIMARY KEY (faculty_id, research_area),
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id)
);

-- HOD
CREATE TABLE HOD (
    hod_id INT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    faculty_count INT,
    uses_digital_tools BIT
);

CREATE TABLE HODCommunication (
    hod_id INT,
    channel VARCHAR(50),
    PRIMARY KEY (hod_id, channel),
    FOREIGN KEY (hod_id) REFERENCES HOD(hod_id)
);

-- COURSE
CREATE TABLE Course (
    course_id INT PRIMARY KEY,
    title VARCHAR(100),
    department VARCHAR(50),
    is_elective BIT,
    semester INT
);

-- ASSIGNMENT
CREATE TABLE Assignment (
    assignment_id INT PRIMARY KEY,
    course_id INT,
    title VARCHAR(100),
    deadline DATE,
    submission_format VARCHAR(50),
    evaluation_method VARCHAR(50),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- COURSE SCHEDULE
CREATE TABLE CourseSchedule (
    schedule_id INT PRIMARY KEY,
    course_id INT,
    faculty_id INT,
    day VARCHAR(20),
    time_slot VARCHAR(20),
    room VARCHAR(20),
    FOREIGN KEY (course_id) REFERENCES Course(course_id),
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id)
);

-- STUDENT SCHEDULE
CREATE TABLE StudentSchedule (
    student_schedule_id INT PRIMARY KEY,
    student_id INT,
    schedule_id INT,
    format_preference VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (schedule_id) REFERENCES CourseSchedule(schedule_id)
);

-- ATTENDANCE
CREATE TABLE Attendance (
    attendance_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    date DATE,
    is_present BIT,
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- GRADE
CREATE TABLE Grade (
    grade_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    assessment_type VARCHAR(50),
    score FLOAT,
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- SUBMISSION
CREATE TABLE Submission (
    submission_id INT PRIMARY KEY,
    assignment_id INT,
    student_id INT,
    submitted_on DATE,
    content VARCHAR(MAX),
    grade FLOAT,
    FOREIGN KEY (assignment_id) REFERENCES Assignment(assignment_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
);

-- MESSAGE
CREATE TABLE Message (
    message_id INT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    sent_at DATETIME,
    message_content VARCHAR(MAX)
);

-- PARENT
CREATE TABLE Parent (
    parent_id INT PRIMARY KEY,
    name VARCHAR(100),
    contact_info VARCHAR(100),
    student_id INT,
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
);

-- TEACHING MATERIAL
CREATE TABLE TeachingMaterial (
    material_id INT PRIMARY KEY,
    faculty_id INT,
    course_id INT,
    title VARCHAR(100),
    content_link VARCHAR(MAX),
    uploaded_on DATE,
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- STUDENT ASSESSMENT
CREATE TABLE StudentAssessment (
    assessment_id INT PRIMARY KEY,
    student_id INT,
    semester INT,
    total_score FLOAT,
    grade VARCHAR(5),
    remarks VARCHAR(MAX),
    updated_at DATETIME,
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
);

-- TEST & RESULT
CREATE TABLE Test (
    test_id INT PRIMARY KEY,
    course_id INT,
    title VARCHAR(100),
    test_date DATE,
    max_marks INT,
    evaluation_method VARCHAR(50),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

CREATE TABLE TestResult (
    result_id INT PRIMARY KEY,
    test_id INT,
    student_id INT,
    marks_obtained FLOAT,
    feedback VARCHAR(MAX),
    FOREIGN KEY (test_id) REFERENCES Test(test_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
);

-- LECTURE
CREATE TABLE Lecture (
    lecture_id INT PRIMARY KEY,
    faculty_id INT,
    course_id INT,
    topic VARCHAR(100),
    delivery_date DATE,
    format VARCHAR(50),
    materials_link VARCHAR(MAX),
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- COURSE COMPLETION
CREATE TABLE CourseCompletion (
    completion_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    status VARCHAR(20),
    completion_date DATE,
    feedback VARCHAR(MAX),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- DISCUSSION BOARD
CREATE TABLE DiscussionBoard (
    post_id INT PRIMARY KEY,
    author_id INT,
    role VARCHAR(20),
    course_id INT,
    content VARCHAR(MAX),
    created_at DATETIME,
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- NOTIFICATION PREFERENCE
CREATE TABLE NotificationPreference (
    preference_id INT PRIMARY KEY,
    user_id INT,
    role VARCHAR(20),
    notify_email BIT,
    notify_sms BIT,
    notify_app BIT
);

-- ASSIGNMENT AI TRAINING DATA
CREATE TABLE AssignmentAITrainingData (
    submission_id INT PRIMARY KEY,
    student_id INT,
    assignment_id INT,
    file_origin VARCHAR(50),
    paste_event_count INT,
    paste_char_max INT,
    paste_violation_flag BIT,
    line_by_line_pattern BIT,
    similarity_score FLOAT,
    plagiarism_flag BIT,
    evaluation_method VARCHAR(50),
    grade_awarded FLOAT,
    feedback_comments VARCHAR(MAX),
    sandbox_mode_used BIT,
    submitted_on DATETIME,
    automation_detected_type VARCHAR(50),
    ethical_intent_flag BIT,
    badge_awarded VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignment(assignment_id)
);
