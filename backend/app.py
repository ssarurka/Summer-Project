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

if __name__ == "__main__":
    app.run(debug=True)