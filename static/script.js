document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("predict-button").addEventListener("click", predictMushroom);
});

function predictMushroom() {
    let mushroom = document.getElementById("mushroom-select").value;
    const resultElement = document.getElementById("result");
    resultElement.innerText = "Checking..."; // Indicate loading

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "mushroom": mushroom })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultElement.innerText = "Error: " + data.error;
            resultElement.style.color = 'red'; //color the error text red.
        } else {
            resultElement.innerText = `Prediction: ${data.prediction}`;
            resultElement.style.color = '#28a745'; //color the result text green.
        }
    })
    .catch(error => {
        console.error("Error:", error);
        resultElement.innerText = "An error occurred.";
        resultElement.style.color = 'red'; //color the error text red.
    });
}