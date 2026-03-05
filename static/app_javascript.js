let selectedInterests = [];

const buttons = document.querySelectorAll(".interests button");

buttons.forEach(btn => {
    btn.addEventListener("click", () => {
        btn.classList.toggle("selected");

        const value = btn.innerText;

        if (selectedInterests.includes(value)) {
            selectedInterests = selectedInterests.filter(i => i !== value);
        } else {
            selectedInterests.push(value);
        }
    });
});

const form = document.querySelector("form");

form.addEventListener("submit", function () {

    if (selectedInterests.length === 0) {
        alert("Please select at least one interest.");
        event.preventDefault();
        return;
    }

    document.getElementById("hiddenInterests").value =
        selectedInterests.join(",");
});