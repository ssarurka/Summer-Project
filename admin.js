BACKEND_URL = "http://127.0.0.1:5000";
DEFAULT_CLASS = 1;

function addDict(dict, ta, review) {
    if (Object.hasOwn(ta)) {
        dict[ta].push(review);
    } else {
        list = [];
        list.push(review);
        dict[ta] = list;
    }
    return dict;
}

async function loadTabs() {
    try {
        response = await fetch(`${BACKEND_URL}/getClasses`);
        data = await response.json();
        classesContainer = document.getElementById('tabsDiv');
        classesContainer.innerHTML = '';
        if (data.success) {
            count = 1;
            data.classes.forEach(classname => {
                line1 = `<input type="radio" name="tabs" id="tab${count}">`;
                line2 = `<label for="tab${count}">${classname.class_name}</label>`
                if (count == 1) line1 = `<input type="radio" name="tabs" id="tab${count}" checked>`;
                else line2 = `<label for="tab${count}" style="border-left: none;">${classname.class_name}</label>`
                classHTML = line1 + line2 + `
                    <div class="tab-content">
                        <h3>${classname.class_name}</h3><hr>
                        <p style="margin-top: 5px;">Choose a TA to view feedback:</p>
                        <select name="tas" id="taDrop">
                        </select>       
                        <button class="selectBtn" id="selectBtn">select</button>
                        <div id="feedback">
                            <p>No feedback</p>
                        </div><hr style="margin-top: 15px;">
                        <div id="ohWrapper">
                            <p style="margin-top: 5px;">Office Hours</p>
					        <table id="office-hours">
                                <tr>
                                    <th>Day of Week</th>
                                    <th>TA name</th>
                                    <th>Time</th>
                                    <th>Location</th>
                                </tr>
                            </table>
				        </div>
                    </div>
                `;
                classesContainer.innerHTML += classHTML;
                count++;
            });
        } else {
            alert(data.message || "Failed to add class.");
        }
    } catch (error) {
        console.error("Error adding class:", error);
    }

    try {
        response = await fetch(`${BACKEND_URL}/getOfficeHours?class=${DEFAULT_CLASS}`);
        data = await response.json();
        table = document.getElementById('office-hours');
        //table.innerHTML = '';
        if (data.success) {
            data.office_hours.forEach(oh => {
                tableHTML = `
                    <tr>
                        <td>${oh.day_of_week}</td>
                        <td>${oh.username}</td>
                        <td>${oh.start_time}-${oh.end_time}</td>
                        <td>${oh.location_name}</td>
                    </tr>
                `;
                table.innerHTML += tableHTML;
            });
        } else {
            alert(data.message || "Failed to add office hour.");
        }
    } catch (error) {
        console.error("Error adding office hour:", error);
    }

    try {
        response = await fetch(`${BACKEND_URL}/getTas?class=${DEFAULT_CLASS}`);
        data = await response.json();
        taContainer = document.getElementById('taDrop');
        taContainer.innerHTML = '';
        if (data.success) {
            data.tas.forEach(ta => {
                taHTML = `
                    <option value="${ta.username}">${ta.username}</option>
                `;
                taContainer.innerHTML += taHTML;
                //console.log(ta.username);
            });
            //console.log("Ta added successfully.");
        } else {
            alert(data.message || "Failed to add ta.");
        }
    } catch (error) {
        console.error("Error adding ta:", error);
    }

    taDropdown = document.getElementById('taDrop');
    selectBtn = document.getElementById('selectBtn');

    feedbacks = {};
    try {
        response = await fetch(`${BACKEND_URL}/getFeedback?class=${DEFAULT_CLASS}`);
        data = await response.json();
        if (data.success) {
            data.fbs.forEach(fb => {
                feedbacks = addDict(feedbacks, fb.username, fb.student_review);
            });
        } else {
            alert(data.message || "Failed to add feedback.");
        }
    } catch (error) {
        console.error("Error adding feedback:", error);
    }

    if (taDropdown && selectBtn) {
        selectBtn.addEventListener('click', () => {
            text = taDropdown.options[taDropdown.selectedIndex].text;
            element = document.getElementById("feedback");
            if (Object.hasOwn(feedbacks, text)) {
                element.textContent = "";
                feedbacks[text].forEach(fb => {
                    element.textContent += fb + "\n";
                });
            } else {
                element.textContent = "No feedback";
            }  
        });
    }
}

document.addEventListener("DOMContentLoaded", function () {
    loadTabs();
    
    homeButton = document.getElementById("homeBtn");
    homeButton.addEventListener("click", function () {
        window.location.href = "adminHomeTabs.html";
    });

    faqButton = document.getElementById("faqBtn");
    faqButton.addEventListener("click", function () {
        window.location.href = "adminFAQ.html";
    });

    signOutButton = document.getElementById("signOutBtn");
    signOutButton.addEventListener("click", function () {
        window.location.href = "adminSignOut.html";
    });

    settingsButton = document.getElementById("settingsBtn");
    settingsButton.addEventListener("click", function () {
        window.location.href = "adminSettings.html";
    });

    menuBtn = document.getElementById('menuBtn');
    navBar = document.getElementById('navBar');
    if (menuBtn && navBar) {
        menuBtn.addEventListener('click', () => {
        navBar.classList.toggle('active');
        });
    }

    faqInput = document.getElementById("faqInput");
    postBtn = document.getElementById("postBtn");
    if (postBtn && faqInput) {
        postBtn.addEventListener("click", async function () {
            textValue = faqInput.value.trim();
            if (textValue === "") {
                alert("Please type a message before posting!");
                return;
            }
            try {
                response = await fetch(`${BACKEND_URL}/addFaq`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        class_id: 1,
                        post: textValue
                    })
                });
                data = await response.json();
                if (data.success) {
                    faqInput.value = "";
                    loadFaqs(); 
                } else {
                    alert(data.message || "Failed to post FAQ.");
                }
            } catch (error) {
                console.error("Error posting FAQ:", error);
            }
        });
    }

    existingRemoveButtons = document.querySelectorAll(".remove_btn_static");
    existingRemoveButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            rowItem = event.target.closest(".faq_item");
            if (rowItem) {
                rowItem.remove();
            }
        });
    });
});