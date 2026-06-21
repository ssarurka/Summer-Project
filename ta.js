document.addEventListener("DOMContentLoaded", function () {
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
    recentFaqContainer = document.querySelector(".recent-faq-container");
    if (postBtn && faqInput && recentFaqContainer) {
        postBtn.addEventListener("click", function () {
            textValue = faqInput.value.trim();
            if (textValue === "") {
                alert("Please type a message before posting!");
                return;
            }
            newFaqItem = document.createElement("div");
            newFaqItem.className = "faq-item";
            newFaqItem.innerHTML = `
                <div class="faq-content-skeleton">
                    <p style="font-family: 'Times New Roman', Times, serif; font-size: 1.1rem; margin: 0; text-align: left;">
                        ${textValue}
                    </p>
                </div>
                <button class="remove-btn-static">REMOVE</button>
            `;
            removeBtn = newFaqItem.querySelector(".remove-btn-static");
            removeBtn.addEventListener("click", function () {
                newFaqItem.remove();
            });
            recentFaqContainer.prepend(newFaqItem);
            faqInput.value = "";
        });
    }
    existingRemoveButtons = document.querySelectorAll(".remove-btn-static");
    existingRemoveButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            rowItem = event.target.closest(".faq-item");
            if (rowItem) {
                rowItem.remove();
            }
        });
    });
});

