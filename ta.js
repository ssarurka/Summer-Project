BACKEND_URL = "http://127.0.0.1:5000";
async function loadFaqs(classId = 1) {
    recentFaqContainer = document.querySelector(".recent_faq_container");
    if (!recentFaqContainer) return;
    try {
        response = await fetch(`${BACKEND_URL}/getFaqs?class_id=${classId}`);
        data = await response.json();
        if (data.success) {
            recentFaqContainer.innerHTML = "";

            data.faqs.forEach(faq => {
                faqHTML = `
                    <div class="faq_item" data-id="${faq.faq_id}">
                        <div class="faq_content_skeleton">
                            <p style="font-family: 'Times New Roman', Times, serif; font-size: 1.1rem; margin: 0; text-align: left;">
                                ${faq.post}
                            </p>
                        </div>
                        <button class="remove_btn_static" onclick="removeFaq(${faq.faq_id})">REMOVE</button>
                    </div>
                `;
                recentFaqContainer.innerHTML += faqHTML;
            });
        }
    } catch (error) {
        console.error("Error loading FAQs:", error);
    }
}

async function removeFaq(faqId) {
    try {
        response = await fetch(`${BACKEND_URL}/removeFaq`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ faq_id: faqId })
        });
        data = await response.json();
        if (data.success) {
            loadFaqs(); // Refresh list automatically
        } else {
            alert(data.message || "Failed to remove FAQ.");
        }
    } catch (error) {
        console.error("Error removing FAQ:", error);
    }
}

async function loadDashboardData() {
    response = await fetch(`${BACKEND_URL}/queueData`);
    data = await response.json();
    if (data.success) {
        document.getElementById("waitTimeValue").innerText = data.projectedWaitTime;
        document.getElementById("studentCountValue").innerText = data.studentsInLine;
        countPercent = Math.min((data.studentsInLine / 12) * 100, 100);
            document.getElementById("studentCountCircle").style.setProperty('--percentage', `${countPercent}%`);
            document.getElementById("waitTimeCircle").style.setProperty('--percentage', `${countPercent}%`);
            container = document.getElementById("queueCardsContainer");
            container.innerHTML = "";
            data.queue.forEach(item => {
                cardHTML = `
                <div class="line_spot">
                    <div class="line_header">
                        <span class="line_number">#${item.queue_number}</span>
                        <span class="line_name">${item.username}</span>
                    </div>
                    <p class="line_body">${item.help_request}</p>
                    <div class="line_footer">
                        <button class="remove_btn" onclick="removeStudent(${item.queue_number})">REMOVE</button>
                    </div>
                </div>
                `;
            container.innerHTML += cardHTML;
        });
    }
}
async function removeStudent(queueNumber) {
    const response = await fetch(`${BACKEND_URL}/removeFromQueue`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ queueNumber: queueNumber })
    });
    const data = await response.json();
    if (data.success) {
        loadDashboardData();
    } else {
        alert(data.message);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    loadDashboardData();
    loadFaqs();

    homeButton = document.getElementById("homeBtn");
    homeButton.addEventListener("click", function () {
        window.location.href = "taHome.html";
    });

    faqButton = document.getElementById("faqBtn");
    faqButton.addEventListener("click", function () {
        window.location.href = "taFaqPosts.html";
    });

    feedbackButton = document.getElementById("feedbackBtn");
    feedbackButton.addEventListener("click", function () {
        window.location.href = "taFeedback.html";
    });

    signOutButton = document.getElementById("signOutBtn");
    signOutButton.addEventListener("click", function () {
        window.location.href = "tempSignOut.html";
    });

    settingsButton = document.getElementById("settingsBtn");
    settingsButton.addEventListener("click", function () {
        window.location.href = "taSettings.html";
    });

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

    menuBtn = document.getElementById('menuBtn');
    navBar = document.getElementById('navBar');
    if (menuBtn && navBar) {
        menuBtn.addEventListener('click', () => {
        navBar.classList.toggle('active');
        });
    }
});







