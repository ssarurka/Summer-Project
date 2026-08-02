from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)
print("CORS ENABLED")

# Replace your MySql password when testing & remove when done
# place holder Password: YOUR_MYSQL_PASSWORD_HERE
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="YOUR_MYSQL_PASSWORD_HERE", 
    database="office_hour_system_application"
)

DEFAULT_ID = 3
DEFAULT_CLASS = 1
TA_ID = 4

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

@app.route("/getClasses", methods=["GET"])
def get_classes_app():
    class_list = get_classes(DEFAULT_ID)
    return jsonify({"success" : True,
                    "classes" : class_list })

@app.route("/getFeedback", methods=["GET"])
def get_feedback_app():
    class_filter = request.args.get('class', '')
    ta_list = get_tas(class_filter)
    feedbacks = []
    for ta in ta_list:
        feedbacks += get_feedback(ta.get('ta_id'), class_filter)
    return jsonify({"success" : True,
                    "fbs" : feedbacks })

@app.route("/getTas", methods=["GET"])
def get_tas_app():
    class_filter = request.args.get('class', '')
    ta_list = get_tas(class_filter)
    return jsonify({"success" : True,
                    "tas" : ta_list })

@app.route("/getOfficeHours", methods=["GET"])
def get_office_hours_app():
    class_filter = request.args.get('class', '')
    oh_list = get_office_hours(class_filter)
    return jsonify({"success" : True,
                    "office_hours" : oh_list })

if __name__ == "__main__":
    app.run(debug=True)