from flask import Flask, request, jsonify
from flask_cors import CORS
import database

app = Flask(__name__)
CORS(app)
print("CORS ENABLED")

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
    
    # create account
    database.create_user(
        email,
        username,
        password,
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
    
    if user["password_hash"] != password:
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
    
    # ask database.py if there is an account with given username & to reset password
    if (database.reset_password(username, password)):
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
    class_id = request.args.get("class_id", 1, type=int)
    metrics = database.get_wait_data(class_id)
    queue_list = database.get_active_queue(class_id)
    return jsonify({
        "success": True,
        "studentsInLine": metrics["students_in_line"],
        "projectedWaitTime": metrics["projected_wait_time"],
        "queue": queue_list
    })

@app.route("/removeFromQueue", methods=["DELETE"])
def remove_from_queue():
    data = request.json
    queue_id = data.get("queue_id")
    rows_deleted = database.remove_from_queue(queue_id)
    if rows_deleted > 0:
        return jsonify({
            "success": True,
            "message": f"Successfully removed."
        })
    else:
        return jsonify({
            "success": False,
            "message": "Student not found or already removed."
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

@app.route("/getClassHeader", methods=["GET"])
def get_class_header():
    class_id = request.args.get("class_id", 1, type=int)
    class_info = database.get_class_by_id(class_id)
    if class_info:
        return jsonify({"success": True, "className": class_info["class_name"]})
    return jsonify({"success": False, "className": "Class"})

if __name__ == "__main__":
    app.run(debug=True, threaded=False)