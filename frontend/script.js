async function getPrediction() {
    let tenure = document.getElementById("tenure").value;
    let monthly_charges = document.getElementById("monthly_charges").value;
    let total_charges = document.getElementById("total_charges").value;

    // ✅ Prevent empty inputs
    if (!tenure || !monthly_charges || !total_charges) {
        alert("Please enter all values before predicting.");
        return;
    }

    try {
        let response = await fetch("https://customerchurn-94x4.onrender.com/predict/", {  // ✅ Local Backend URL
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

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        let result = await response.json();
        console.log("Response from backend:", result);  // ✅ Debugging in Console
        document.getElementById("prediction-result").innerText = "Prediction: " + (result.prediction || "Error in prediction");

    } catch (error) {
        console.error("Error:", error);
        document.getElementById("prediction-result").innerText = "Error getting prediction.";
    }
}
