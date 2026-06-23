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
});
