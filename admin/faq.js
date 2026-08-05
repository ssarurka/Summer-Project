document.addEventListener("DOMContentLoaded", function () {    
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
});