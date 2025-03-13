let currentPage = 0;
const pages = document.querySelectorAll('.page');

function nextPage() {
    if (currentPage < pages.length - 1) {
        currentPage++;
        updatePage();

        if (currentPage === 2) {
            setTimeout(fetchTesters, 500);
        }
    }
}

function updatePage() {
    pages.forEach((page, index) => {
        page.style.display = index === currentPage ? "block" : "none";
    });
}

function updateEmailLink() {
    fetch("/send_email")
        .then(response => response.json())
        .then(data => {
            document.getElementById("configureLink").href = data.link;
        })
        .catch(error => console.error("Error fetching email link:", error));
}


document.addEventListener("DOMContentLoaded", updateEmailLink);

function copyToClipboard() {
    const textField = document.querySelector(".copy-text");
    textField.select();
    navigator.clipboard.writeText(textField.value).then(() => {
        alert("Link copied to clipboard!");
    });
}

function submitForm() {
    const branchName = document.getElementById("branch_name").value;
    const numCommits = document.getElementById("number_of_commits").value;
    const runButton = document.getElementById("runButton");
    const progressBarContainer = document.getElementById("progressBarContainer");
    const progressBar = document.getElementById("progressBar");

    if (!branchName || !numCommits) {
        alert("Please enter all required details.");
        return;
    }

    runButton.style.display = "none";
    progressBarContainer.style.display = "block";
    progressBar.style.width = "0%";

    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 10;
        progressBar.style.width = `${progress}%`;

        if (progress >= 90) {
            clearInterval(progressInterval);
        }
    }, 500);

    fetch("/run", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `branch_name=${encodeURIComponent(branchName)}&number_of_commits=${encodeURIComponent(numCommits)}`
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.detail || "Error occurred!");
            });
        }
        return response.text();
    })
    .then(html => {
        clearInterval(progressInterval);
        progressBar.style.width = "100%";

        setTimeout(() => {
            progressBarContainer.style.display = "none";
            runButton.style.display = "block";

            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");

            document.getElementById("suggestedTest").textContent = doc.querySelector("#suggestedTest")?.textContent || "";
            document.getElementById("suggestedRecipe").textContent = doc.querySelector("#suggestedRecipe")?.textContent || "";

            currentPage = 1;
            updatePage();

            
            updateEmailLink();
        }, 500);
    })
    .catch(error => {
        clearInterval(progressInterval);
        alert(error.message);
        progressBarContainer.style.display = "none";
        runButton.style.display = "block";
    });
}

document.getElementById("runForm").addEventListener("submit", function(event) {
    event.preventDefault();
    submitForm();
});

function fetchTesters() {
    fetch("/get_agents")
    .then(response => response.json())
    .then(data => {
        const testerDropdown = document.getElementById("actionChoice");
        testerDropdown.innerHTML = "";

        data.tester.forEach(tester => {
            let option = document.createElement("option");
            option.value = tester;
            option.textContent = tester;
            testerDropdown.appendChild(option);
        });
    })
    .catch(error => console.error("Error fetching testers:", error));
}

function runFinalScript() {
    const selectedTester = document.getElementById("actionChoice").value;

    fetch("/run_final", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `tester=${encodeURIComponent(selectedTester)}`
    })
    .then(response => response.json())
    .then(data => {
        console.log("Final script output:", data.output);
        alert("build triggered successfully!");
        currentPage = 3;
        updatePage();
    })
    .catch(error => console.error("Error triggering build:", error));
}
