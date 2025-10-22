CREATE VIEW StudentReportView AS
SELECT 
    sd.student_id,
    sd.student_name,
    sd.father_name,
    sd.branch_id,
    sd.college_name,
    sd.gender,
    sd.dob,
    sd.category,
    sd.sub_category,
    sa.current_sem,
    sa.cgpa,
    sa.grade,
    sa.status
FROM 
    StudentDetails sd
JOIN 
    StudentAcademic sa ON sd.student_id = sa.student_id;