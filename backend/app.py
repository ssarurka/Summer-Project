from flask import Flask, request, jsonify
from flask_cors import CORS
import database
import bcrypt

app = Flask(__name__)
CORS(app)
print("CORS ENABLED")

def hash_password(password):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(pwd_bytes, salt)
    return hash_pwd.decode("utf-8")

def verify_password(stored_hash, input_password):
    return bcrypt.checkpw(input_password.encode("utf-8"), stored_hash.encode("utf-8"))


@app.route("/createAccount", methods=["POST"])
def create_account():
    data = request.json
    email = data["email"]
    username = data["username"]
    password = data["password"]
    account_type = data["accountType"]

    # ask database.py if username already exists
    if database.username_exists(username):
        return jsonify({
            "success": False,
            "message": "Username already exists."
        })
    
    #ask database.py if email already exist
    if database.email_exists(email):
        return jsonify({
            "success": False,
            "message": "Email already exists."
        })
    hash_pwd = hash_password(password)
    # create account
    database.create_user(
        email,
        username,
        hash_pwd,
        account_type
    )

    return jsonify({
        "success": True,
        "message": "Account created."
    })

@app.route("/login", methods=["POST"])
def handle_login():
    data = request.json
    username = data["username"]
    password = data["password"]
    
    # ask database.py if there is an account with given username & password
    user = database.get_user(username)

    if user is None:
        return jsonify({
                "success": False,
                "message": "Username does not exist"
            })
    
    if not verify_password(user["password_hash"], password):
        return jsonify({
            "success": False,
            "message": "Incorrect Password"
        })
    
    return jsonify({
        "success": True,
        "message": "Login successful",
        "accountType": user["account_type"],
        "userId": user["user_id"]
    })
        
@app.route("/resetPassword", methods=["PATCH"])
def handle_reset_password():
    print("=== Reset password route reached ===")

    data = request.json
    print(data)

    username = data["username"]
    password = data["password"]
    email = data["email"]

    user = database.get_user(username)
    print(user)
    if user is None:
        return jsonify({
            "success": False,
            "message": "Username does not exist"
        })
    
    if user["email"] != email:
        return jsonify({
            "success": False,
            "message": "Incorrect Email"
        })
    hashed_pwd = hash_password(password)
    # ask database.py if there is an account with given username & to reset password
    if (database.reset_password(username, hashed_pwd)):
        return jsonify({
            "success": True,
            "message": "Password is Reset"
        })
    else :
        return jsonify({
            "success": False,
            "message": "Password was unable to be reset"
        })

@app.route("/queueData", methods=["GET"])
def get_queue_data():
    metrics = database.get_wait_data()
    queue_list = database.get_active_queue()
    return jsonify({
        "success": True,
        "studentsInLine": metrics["students_in_line"],
        "projectedWaitTime": metrics["projected_wait_time"],
        "queue": queue_list
    })

@app.route("/removeFromQueue", methods=["DELETE"])
def remove_from_queue():
    data = request.json
    queue_number = data.get("queueNumber")
    rows_deleted = database.remove_from_queue(queue_number)
    if rows_deleted > 0:
        return jsonify({
            "success": True,
            "message": f"Successfully removed position #{queue_number} from the line."
        })
    else:
        return jsonify({
            "success": False,
            "message": "Queue position not found or already removed."
        })

@app.route("/getFaqs", methods=["GET"])
def get_faqs():
    class_id = request.args.get("class_id", 1)
    faqs = database.get_faqs(class_id)
    return jsonify({
        "success": True,
        "faqs": faqs
    })

@app.route("/addFaq", methods=["POST"])
def add_faq():
    data = request.json
    post_text = data.get("post")
    class_id = data.get("class_id", 1)
    if not post_text:
        return jsonify({
            "success": False,
            "message": "FAQ post content cannot be empty."
        }), 400
    rows_inserted = database.add_faq(class_id, post_text)
    if rows_inserted > 0:
        return jsonify({
            "success": True,
            "message": "FAQ posted successfully."
        })
    else:
        return jsonify({
            "success": False,
            "message": "Failed to post FAQ."
        })

@app.route("/removeFaq", methods=["DELETE"])
def remove_faq():
    data = request.json
    faq_id = data.get("faq_id")
    rows_deleted = database.remove_faq(faq_id)
    if rows_deleted > 0:
        return jsonify({
            "success": True,
            "message": "FAQ removed successfully."
        })
    else:
        return jsonify({
            "success": False,
            "message": "FAQ position not found or already deleted."
        })

@app.route("/createOH", methods=["POST"])
def create_office_hour_app():
    data = request.json
    class_name = data["class_id"]
    dow = data["dow"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    loc = data["loc"]


    # create oh
    database.create_office_hour(
        class_name,
        dow,
        start_time,
        end_time,
        loc
    )

    return jsonify({
        "success": True,
        "message": "Office Hour created."
    })

@app.route("/getClass", methods=["GET"])
def get_class_app():
    class_filter = request.args.get('name', '')
    class_list = database.get_class(class_filter)
    return jsonify({"success" : True,
                    "classes" : class_list })

@app.route("/getClasses", methods=["GET"])
def get_classes_app():
    class_list = database.get_classes(database.DEFAULT_ID)
    return jsonify({"success" : True,
                    "classes" : class_list })

@app.route("/getFeedback", methods=["GET"])
def get_feedback_app():
    class_filter = request.args.get('class', '')
    ta_list = database.get_tas(class_filter)
    feedbacks = []
    for ta in ta_list:
        feedbacks += database.get_feedback(ta.get('ta_id'), class_filter)
    return jsonify({"success" : True,
                    "fbs" : feedbacks })

@app.route("/getTas", methods=["GET"])
def get_tas_app():
    class_filter = request.args.get('class', '')
    ta_list = database.get_tas(class_filter)
    return jsonify({"success" : True,
                    "tas" : ta_list })

@app.route("/getOfficeHours", methods=["GET"])
def get_office_hours_app():
    class_filter = request.args.get('class', '')
    oh_list = database.get_office_hours(class_filter)
    return jsonify({"success" : True,
                    "office_hours" : oh_list })

if __name__ == "__main__":
    app.run(debug=True, threaded=False)