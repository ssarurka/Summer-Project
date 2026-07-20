import mysql.connector
# Replace your MySql password when testing & remove when done
# place holder Password: YOUR_MYSQL_PASSWORD_HERE
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD_HERE", 
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