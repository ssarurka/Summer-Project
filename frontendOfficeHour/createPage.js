const submitButton = document.getElementById("submitLog")
submitButton.addEventListener("click", createAccount)
// Reads values from the form
function getFormData() {
    return {
        email:
        document.getElementById("emailCre").value,

        username:
        document.getElementById("usernameCre").value,

        password:
        document.getElementById("passwordCre").value,

        accountType:
        document.querySelector(
            'input[name="accountType"]:checked'
        )?.value
    };
}

// Runs when user presses Create Account
async function createAccount() {
    let data = getFormData()

    if(!validateRequiredFields(data)){
        return;
    }

    if(!validatePurdueEmail(data.email)){
        return;
    }

    if(!validatePassword(data.password)){
        return;
    }
    await sendCreateAccountRequest(data);

}

// Makes sure every field is filled in
function validateRequiredFields(data) {
    if (!data.email ) {
        alert("Username is required");
        return false;
    }

    if (!data.password) {
        alert("Password is required");
        return false;
    }

    if (!data.email) {
        alert("A Purdue Email is required");
        return false;
    }

    if (!data.accountType) {
        alert("Please select an account type");
        return false;
    }
    return true;
}

// Checks @purdue.edu email
function validatePurdueEmail(email) {
    const regex = /^[a-zA-Z0-9._%+-]+@purdue\.edu$/;   

    if(!regex.test(email)) {
        alert("Please enter a valid Purdue email");
        return false;
    }
    return true;
}

// Checks password requirements
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


// Sends data to Flask
async function sendCreateAccountRequest(data) {
    let response = await fetch(
        "http://127.0.0.1:5000/createAccount",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        }
    );
    let result = await response.json();

    if (result.success) {
        alert("Account Created. Please log in.");
    }
    else {
        alert(result.message);
    }
}