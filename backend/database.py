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



