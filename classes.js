// Classes are kept in localStorage for now so they survive a page refresh.
// This will get swapped out for real backend calls once that part is wired up -
// but for now, everything here is 100% frontend.

const STORAGE_KEY = "myClasses";

function loadClassesFromStorage() {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    try {
        return JSON.parse(raw);
    } catch (e) {
        return [];
    }
}

function saveClassesToStorage(classes) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(classes));
}

let classes = loadClassesFromStorage();

function openAddClassModal() {
    document.getElementById("classNameInput").value = "";
    document.getElementById("addClassModal").classList.remove("hidden");
    document.getElementById("classNameInput").focus();
}

function closeAddClassModal() {
    document.getElementById("addClassModal").classList.add("hidden");
}

function submitAddClass() {
    const nameInput = document.getElementById("classNameInput");
    const className = nameInput.value.trim();

    if (!className) {
        alert("Please enter a class name.");
        return;
    }

    classes.push({
        id: Date.now(),
        name: className
    });

    saveClassesToStorage(classes);
    renderClasses();
    closeAddClassModal();
}

function buildClassCard(classInfo) {
    const template = document.getElementById("classCardTemplate");
    const card = template.content.firstElementChild.cloneNode(true);

    card.querySelector(".class-title").textContent = classInfo.name;

    const officeHoursLink = card.querySelector(".office-hours-link");
    const taReviewsLink = card.querySelector(".ta-reviews-link");
    const faqLink = card.querySelector(".faq-link");

    officeHoursLink.href = `officeHours.html?class_id=${classInfo.id}`;
    taReviewsLink.href = `taReviews.html?class_id=${classInfo.id}`;
    faqLink.href = `faq.html?class_id=${classInfo.id}`;

    card.querySelector(".delete-class-btn").addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        deleteClass(classInfo.id);
    });

    return card;
}

function deleteClass(classId) {
    classes = classes.filter(c => c.id !== classId);
    saveClassesToStorage(classes);
    renderClasses();
}

function renderClasses() {
    const grid = document.getElementById("classesGrid");
    const emptyState = document.getElementById("emptyState");

    grid.innerHTML = "";

    if (classes.length === 0) {
        emptyState.classList.remove("hidden");
        return;
    }

    emptyState.classList.add("hidden");

    classes.forEach(classInfo => {
        grid.appendChild(buildClassCard(classInfo));
    });
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("addClassBtn").addEventListener("click", openAddClassModal);
    document.getElementById("cancelAddClassBtn").addEventListener("click", closeAddClassModal);
    document.getElementById("confirmAddClassBtn").addEventListener("click", submitAddClass);

    document.getElementById("classNameInput").addEventListener("keydown", (event) => {
        if (event.key === "Enter") submitAddClass();
    });

    document.getElementById("addClassModal").addEventListener("click", (event) => {
        if (event.target.id === "addClassModal") {
            closeAddClassModal();
        }
    });

    renderClasses();
});