async function checkJob() {
    const text = document.getElementById("jobText").value;
    const resultDiv = document.getElementById("result");

    if (!text.trim()) {
        resultDiv.innerHTML = "Please enter job description.";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                job_description: text
            })
        });

        const data = await response.json();

        resultDiv.style.display = "block"; // Make sure it's visible
        resultDiv.innerHTML = `
            <b>Prediction:</b> ${data.prediction}<br>
            <b>Confidence:</b> ${data.confidence}
            ${data.reason ? `<br><span style="color:red">Reason: ${data.reason}</span>` : ""}
        `;

        // Store result for flagging
        window.lastResult = data;
        window.lastJobDescription = text;

        // Show flag button
        const flagSection = document.getElementById("flag-section");
        flagSection.classList.remove("hidden");
        flagSection.style.display = "block"; // Backup in case class is missing

        document.getElementById("flag-form").classList.add("hidden"); // Reset form state
        document.getElementById("flag-form").style.display = "none";

    } catch (error) {
        resultDiv.style.display = "block";
        resultDiv.innerHTML =
            "<span style='color:red'>Unable to connect to backend. Make sure backend is running.</span>";
    }
}

function showFlagForm() {
    const form = document.getElementById("flag-form");
    form.classList.remove("hidden");
    form.style.display = "block";
}

async function submitFlag() {
    const reason = document.getElementById("flag-reason").value;
    if (!reason && !confirm("Submit without a reason?")) return;

    try {
        const response = await fetch("http://127.0.0.1:8000/flag", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                job_description: window.lastJobDescription,
                prediction: window.lastResult.prediction,
                confidence: window.lastResult.confidence,
                reason: reason || "User marked as incorrect"
            })
        });
        const resData = await response.json();
        alert(resData.message);
        document.getElementById("flag-section").classList.add("hidden");
        document.getElementById("flag-section").style.display = "none";
    } catch (error) {
        alert("Failed to submit flag.");
    }
}
