INSERT INTO users (user_id, email, username, password_hash, account_type) VALUES
(1, 'abby@purdue.edu', 'Abby', 'pass_1', 'student'),
(2, 'shreeya@purdue.edu', 'Shreeya', 'pass_2', 'student'),
(3, 'parul@purdue.edu', 'Parul', 'pass_3', 'student'),
(4, 'samaika@purdue.edu', 'Samaika', 'pass_4', 'student');
(5, 'prisha@purdue.edu', 'Prisha', 'pass_5', 'student');
(6, 'shannon@purdue.edu', 'Shannon', 'pass_6', 'student');

INSERT INTO student_help_queue (queue_number, student_id, help_request) VALUES
(1, 1, 'I keep getting a segmentation fault on read_data()...'),
(2, 2, 'I keep getting a segmentation fault on read_data()...'),
(3, 3, 'I keep getting a segmentation fault on read_data()...'),
(4, 4, 'I keep getting a segmentation fault on read_data()...');
(5, 5, 'I keep getting a segmentation fault on read_data()...');
(6, 6, 'I keep getting a segmentation fault on read_data()...');