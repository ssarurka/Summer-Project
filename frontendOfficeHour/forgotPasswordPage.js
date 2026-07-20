const enterBtn = document.getElementById("submitReset")
enterBtn.addEventListener("click", resetPassword)

async function resetPassword() {
    let data = getResetData();

    if (!validateRequiredFields(data)) {
        return;
    }
    if (!validateEmail(data.email)) {
        return;
    }
    if (!validatePassword(data.password)) {
        return;
    }
    if (!validatePasswordMatch(data.password, data.confirmPassword)) {
        return;
    }
    await sendResetRequest(data);
}

// get the data in the form
function getResetData() {
    return {
        email: 
        document.getElementById("emailReset").value,
        username: 
        document.getElementById("usernameReset").value,
        password: 
        document.getElementById("passwordReset").value,
        confirmPassword: 
        document.getElementById("passwordConReset").value
    };
}

// check if the values in fields are valid
function validateRequiredFields(data) {
    if (!data.email) {
        alert("A Purdue Email is required");
        return false;
    }

    if (!data.username) {
        alert("Username is required");
        return false;
    }

    if (!data.password) {
        alert("Password is required");
        return false;
    }

    if (!data.confirmPassword) {
        alert("Please re enter new password");
        return false;
    }
    return true;
}

// check that email entered is a purdue email
function validateEmail(email) {
    const regex = /^[a-zA-Z0-9._%+-]+@purdue\.edu$/;   

    if(!regex.test(email)) {
        alert("Please enter a valid Purdue email");
        return false;
    }
    return true;
}

// check that password matches requirements
function validatePassword(password) {
    const regex = /^(?=.*[A-Z])(?=.*[\W_]).{8,}$/;
    if (!regex.test(password)) {
        alert(
            "Password must contain at least 8 characters, one uppercase letter, and one special character"
        );
        return false;
    }
    return true;
}

// checks that data in both fields match
function validatePasswordMatch(password, confirmPassword) {
    if (password !== confirmPassword) {
        alert(
            "Data in Password Field and Confirm Password Field don't match"
        );
        return false;
    }
    return true;
}

// send data to Flask to change password
async function sendResetRequest(data) {
    console.log("sending request", data);
    
    let response = await fetch(
        "http://127.0.0.1:5000/resetPassword",
        {
            method: "PATCH",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        }
    );
    let result = await response.json();

    if (result.success) {
        alert("Password Reset. Please log in.");
    }
    else {
        alert(result.message);
    }
}