document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("clickBtn");
    const message = document.getElementById("message");

    button.addEventListener("click", function () {
        const now = new Date();
        message.textContent = "Button clicked at: " + now.toLocaleTimeString();
    });
});