document.addEventListener("DOMContentLoaded", () => {
    const taskInput = document.getElementById("taskInput");
    const addTaskBtn = document.getElementById("addTaskBtn");
    const taskList = document.getElementById("taskList");

    addTaskBtn.addEventListener("click", addTask);
    taskInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            addTask();
        }
    });

    function addTask() {
        const taskText = taskInput.value.trim();
        if (taskText !== "") {
            const listItem = document.createElement("li");
            listItem.innerHTML = `
                <span>${taskText}</span>
                <span class="completion-time"></span>
                <button>Delete</button>
            `;

            taskList.appendChild(listItem);
            taskInput.value = "";

            // Add event listener for toggling completion
            listItem.querySelector("span").addEventListener("click", () => {
                listItem.classList.toggle("completed");
                const completionTimeSpan = listItem.querySelector(".completion-time");
                if (listItem.classList.contains("completed")) {
                    const now = new Date();
                    const formattedTime = now.toLocaleString(); // e.g., "M/D/YYYY, H:MM:SS AM/PM"
                    completionTimeSpan.textContent = `(Completed: ${formattedTime})`;
                } else {
                    completionTimeSpan.textContent = ""; // Clear time if un-completed
                }
            });

            // Add event listener for deleting task
            listItem.querySelector("button").addEventListener("click", () => {
                taskList.removeChild(listItem);
            });
        }
    }
});