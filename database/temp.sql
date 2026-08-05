INSERT INTO users (user_id, email, username, password_hash, account_type) VALUES 
(1, 'abby@purdue.edu', 'Abby', 'pass_1', 'student'), 
(2, 'shreeya@purdue.edu', 'Shreeya', 'pass_2', 'student'), 
(3, 'parul@purdue.edu', 'Parul', 'pass_3', 'student'), 
(4, 'samaika@purdue.edu', 'Samaika', 'pass_4', 'student'),
(5, 'prisha@purdue.edu', 'Prisha', 'pass_5', 'student'),
(6, 'shannon@purdue.edu', 'Shannon', 'pass_6', 'student');

INSERT INTO classes (class_id, class_name, class_semester, class_admin, class_code_hash) VALUES
(1, 'CS240', 'Fall 2026', 1, 'hash_code_123');

INSERT INTO student_help_queue (class_id, student_id, help_request, check_in_time) VALUES 
(1, 1, 'I keep getting a segmentation fault on read_data()...', '2026-08-05 10:00:00'),
(1, 2, 'I keep getting a segmentation fault on read_data()...', '2026-08-05 10:05:00'),
(1, 3, 'I keep getting a segmentation fault on read_data()...', '2026-08-05 10:10:00'),
(1, 4, 'I keep getting a segmentation fault on read_data()...', '2026-08-05 10:15:00'),
(1, 5, 'I keep getting a segmentation fault on read_data()...', '2026-08-05 10:20:00'), 
(1, 6, 'I keep getting a segmentation fault on read_data()...', '2026-08-05 10:25:00');