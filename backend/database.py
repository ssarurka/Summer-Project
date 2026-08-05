import mysql.connector
# Replace your MySql password when testing & remove when done
# place holder Password: YOUR_MYSQL_PASSWORD_HERE
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="FMSJaguar0208!", 
    database="office_hour_system_application"
)

def username_exists(username):
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = %s",
        (username,)
    )
    user = cursor.fetchone()
    cursor.close()
    if user is None:
        return False
    else:
        return True
    
def email_exists(email):
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = %s",
        (email,)
    )
    found = cursor.fetchone()
    cursor.close()
    if found is None:
        return False
    else:
        return True
   

def create_user(email, username, password, account_type):
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO users
        (email, username, password_hash, account_type)
        VALUES (%s, %s, %s, %s)
        """,
        (email, username, password, account_type,)
    )
    connection.commit()
    cursor.close()


def get_user(username):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE username = %s",
        (username,)
    ) 
    user = cursor.fetchone()
    cursor.close()
    return user


def reset_password(username, password):
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE users
        SET password_hash = %s
        WHERE username = %s
        """,
        (password, username)
    ) 
    rows_updated = cursor.rowcount
    connection.commit()
    cursor.close()
    
    return rows_updated

def get_wait_data():
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) as total FROM student_help_queue"
    )
    result = cursor.fetchone()
    student_count = result[0] if result else 0
    AVG_MINUTES_PER_STUDENT = 20
    total_minutes = student_count * AVG_MINUTES_PER_STUDENT
    hours = total_minutes // 60
    minutes = total_minutes % 60
    projected_wait_time = f"{hours}:{minutes:02d}"
    cursor.close()
    return {
        "students_in_line": student_count,
        "projected_wait_time": projected_wait_time
    }

def get_active_queue():
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT 
            q.queue_number, 
            u.username, 
            q.help_request 
        FROM student_help_queue q
        JOIN users u ON q.student_id = u.user_id
        ORDER BY q.queue_number ASC
        """
    )
    queue_list = cursor.fetchall()
    cursor.close()
    return queue_list

def remove_from_queue(queue_number):
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM student_help_queue WHERE queue_number = %s",
        (queue_number,)
    )
    connection.commit()
    rows_deleted = cursor.rowcount
    cursor.close()
    return rows_deleted

def get_faqs(class_id=1):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT faq_id, class_id, post, creation_time 
        FROM faqs 
        WHERE class_id = %s 
        ORDER BY creation_time DESC
        """,
        (class_id,)
    )
    faq_list = cursor.fetchall()
    cursor.close()
    return faq_list

def add_faq(class_id, post_text):
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO faqs (class_id, post) 
        VALUES (%s, %s)
        """,
        (class_id, post_text)
    )
    connection.commit()
    rows_inserted = cursor.rowcount
    cursor.close()
    return rows_inserted

def remove_faq(faq_id):
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM faqs WHERE faq_id = %s",
        (faq_id,)
    )
    connection.commit()
    rows_deleted = cursor.rowcount
    cursor.close()
    return rows_deleted

def get_classes(admin_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT class_id, class_name, class_semester 
        FROM classes 
        WHERE class_admin = %s
        """,
        (admin_id, )
    )
    class_list = cursor.fetchall()
    cursor.close()
    return class_list

def get_class(class_name):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT class_id
        FROM classes 
        WHERE class_name = %s
        """,
        (class_name, )
    )
    class_list = cursor.fetchall()
    cursor.close()
    return class_list

def get_tas(class_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT ta_classes.ta_id, users.username
        FROM ta_classes
        INNER JOIN users ON ta_classes.ta_id = users.user_id
        WHERE ta_classes.class_id = %s
        """,
        (class_id, )
    )
    ta_list = cursor.fetchall()
    cursor.close()
    return ta_list

def get_feedback(ta_id, class_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT users_ta_reviews.student_review, users_ta_reviews.creation_time, users_ta_reviews.ta_id, users.username, users.email
        FROM users_ta_reviews INNER JOIN users
        ON users_ta_reviews.ta_id = users.user_id
        WHERE users_ta_reviews.class_id = %s AND users_ta_reviews.ta_id = %s
        ORDER BY users_ta_reviews.creation_time DESC
        """,
        (class_id, ta_id, )
    )
    ta_list = cursor.fetchall()
    cursor.close()
    return ta_list

def get_feedback_name(ta_name, class_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT users_ta_reviews.student_review, users_ta_reviews.creation_time, users_ta_reviews.ta_id, users.username, users.email
        FROM users_ta_reviews INNER JOIN users
        ON users_ta_reviews.ta_id = users.user_id
        WHERE users_ta_reviews.class_id = %s AND users.username = %s
        """,
        (class_id, ta_name, )
    )
    ta_list = cursor.fetchall()
    cursor.close()
    return ta_list

def get_office_hours(class_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT office_hours.day_of_week, office_hours.start_time, office_hours.end_time, users.username, locations.location_name
        FROM  office_hours
        INNER JOIN ta_office_hours ON ta_office_hours.office_hour_id = office_hours.office_hour_id
        INNER JOIN locations ON locations.location_id = office_hours.location_id
        INNER JOIN users ON ta_office_hours.ta_id = users.user_id
        WHERE office_hours.class_id = %s
        """,
        (class_id, )
    )
    oh_list = cursor.fetchall()
    cursor.close()
    return oh_list

def get_location_id(location_name):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT location_id
        FROM locations
        WHERE location_name = %s
        """,
        (location_name,)
    )
    loc = cursor.fetchall()
    cursor.close()
    return loc

def create_location(location_name):
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO locations
        VALUES (DEFAULT, %s)
        """,
        (location_name,)
    )
    connection.commit()
    cursor.close()

def create_office_hour(class_id, day_of_week, start_time, end_time, location_name):
    loc =  get_location_id(location_name)
    if (len(loc) < 1):
        create_location(location_name)
        loc = get_location_id(location_name)[0][0]
    else:
        loc = loc[0][0]
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO office_hours
        VALUES (DEFAULT, %s, %s, %s, %s, %s, DEFAULT, DEFAULT)
        """,
        (class_id, day_of_week, start_time, end_time, loc,)
    )
    connection.commit()
    cursor.close()