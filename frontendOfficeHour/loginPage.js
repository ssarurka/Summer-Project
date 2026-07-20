const enterBtn = document.getElementById("submitLog")
enterBtn.addEventListener("click", login)

// sends data to Flask to see if can login
async function login() {
    let data = getLoginData();
    if (!validateLoginFields(data)) {
        return;
    }
    await sendLoginRequest(data);
}

// gets data from the form
function getLoginData() {
    return {
        username:
        document.getElementById("usernameLog").value,

        password:
        document.getElementById("passwordLog").value,
    };
}

// checks that values are entered in fields
async function validateLoginFields(data) {
    if (data.username == "") {
        alert("Username is required");
        return false;
    }
    if (data.password == "") {
        alert("Password is required");
        return false;
    }
  
    return true;
}

// Talk to Flask see if entered data is correct/ matches an account
//----- TODO: Redirect user to the correct page based on account type (student, TA, admin)!--------|
async function sendLoginRequest(data) {
    let response = await fetch(
        "http://127.0.0.1:5000/login",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        }
    );
    let result = await response.json();

    if (!result.success) {
        alert(result.message);
    }
    else {
        alert("Login successful")
    }
}