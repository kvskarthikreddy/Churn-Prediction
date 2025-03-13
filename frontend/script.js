async function getPrediction() {
    let tenure = document.getElementById("tenure").value;
    let monthly_charges = document.getElementById("monthly_charges").value;
    let total_charges = document.getElementById("total_charges").value;

    let response = await fetch("https://customer-churn-api-v1.onrender.com", {  // 🔹 Updated Render URL
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            tenure: parseFloat(tenure),
            monthly_charges: parseFloat(monthly_charges),
            total_charges: parseFloat(total_charges)
        })
    });

    let result = await response.json();
    document.getElementById("prediction-result").innerText = "Prediction: " + result.prediction;
}
