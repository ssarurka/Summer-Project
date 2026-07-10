USE office_hour_system_application;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(10) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    account_type ENUM('student', 'ta', 'admin') NOT NULL
);

CREATE TABLE classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(20) NOT NULL,
    class_semester VARCHAR(15) NOT NULL,
    class_admin INT NOT NULL,
    class_code_hash VARCHAR(255) NOT NULL,

    FOREIGN KEY(class_admin) REFERENCES users(user_id)
);

CREATE TABLE student_classes (
    student_id INT NOT NULL,
    class_id INT NOT NULL,

    PRIMARY KEY(student_id, class_id),
    FOREIGN KEY(student_id) REFERENCES users(user_id),
    FOREIGN KEY(class_id) REFERENCES classes(class_id)
);

CREATE TABLE ta_classes (
    ta_id INT NOT NULL,
    class_id INT NOT NULL,

    PRIMARY KEY(ta_id, class_id),
    FOREIGN KEY(ta_id) REFERENCES users(user_id),
    FOREIGN KEY(class_id) REFERENCES classes(class_id)
);

CREATE TABLE locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(40) NOT NULL
);

CREATE TABLE office_hours (
    office_hour_id INT AUTO_INCREMENT PRIMARY KEY,
    class_id INT NOT NULL,
    day_of_week ENUM('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    location_id INT NOT NULL,
    ta_capacity INT NOT NULL DEFAULT 4,
    cur_ta_count INT NOT NULL DEFAULT 0,

    FOREIGN KEY(class_id) REFERENCES classes(class_id),
    FOREIGN KEY(location_id) REFERENCES locations(location_id)
);

CREATE TABLE ta_office_hours (
    ta_id INT NOT NULL,
    office_hour_id INT NOT NULL,

    PRIMARY KEY(ta_id, office_hour_id),
    FOREIGN KEY(ta_id) REFERENCES users(user_id),
    FOREIGN KEY(office_hour_id) REFERENCES office_hours(office_hour_id)
);

CREATE TABLE faqs (
    faq_id INT AUTO_INCREMENT PRIMARY KEY,
    class_id INT NOT NULL,
    post TEXT NOT NULL,
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(class_id) REFERENCES classes(class_id)
);

CREATE TABLE users_ta_reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    student_review TEXT NOT NULL,
    ta_id INT NOT NULL,
    class_id INT NOT NULL,
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(student_id) REFERENCES users(user_id),
    FOREIGN KEY(ta_id) REFERENCES users(user_id),
    FOREIGN KEY(class_id) REFERENCES classes(class_id)
);

CREATE TABLE student_help_queue (
    queue_id INT AUTO_INCREMENT PRIMARY KEY,
    queue_number INT NOT NULL UNIQUE,
    check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    student_id INT NOT NULL,
    help_request TEXT NOT NULL,

    FOREIGN KEY(student_id) REFERENCES users(user_id)
);