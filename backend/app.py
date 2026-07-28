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


if __name__ == "__main__":
    app.run(debug=True)