import mysql.connector
# Replace your MySql password when testing & remove when done
# place holder Password: YOUR_MYSQL_PASSWORD_HERE
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="5k7Bc4fU49Ty$$u", 
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

def get_wait_data(class_id=1):
    cursor = connection.cursor(buffered=True)
    cursor.execute(
        "SELECT COUNT(*) as total FROM student_help_queue WHERE class_id = %s",
        (class_id,)
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

def get_active_queue(class_id=1):
    cursor = connection.cursor(buffered=True, dictionary=True)
    cursor.execute(
        """
        SELECT 
            q.queue_id, 
            u.username, 
            q.help_request,
            q.check_in_time
        FROM student_help_queue q
        JOIN users u ON q.student_id = u.user_id
        WHERE q.class_id = %s
        ORDER BY q.check_in_time ASC
        """,
        (class_id,)
    )
    queue_list = cursor.fetchall()
    cursor.close()
    for index, entry in enumerate(queue_list, start=1):
        entry["display_number"] = index
    return queue_list

def remove_from_queue(queue_id):
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM student_help_queue WHERE queue_id = %s",
        (queue_id,)
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

def get_class_by_id(class_id):
    cursor = connection.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT class_name FROM classes WHERE class_id = %s", (class_id,))
    result = cursor.fetchone()
    cursor.close()
    return result