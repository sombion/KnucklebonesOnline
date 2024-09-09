document.addEventListener("DOMContentLoaded", function() {
    let statusText = document.querySelector(".loading-status");
    let currentStep = 1;

    /*setInterval(function() {
        currentStep = currentStep === 1 ? 2 : 1;
        statusText.textContent = `${currentStep}/2`;
    }, 3000); // Переход между 1 и 2 каждые 3 секунды
    */
});

function cancelLoading() {
    window.location.href = "/"; // Здесь укажите путь к главной странице
}


var ws = new WebSocket(`ws://localhost:8000/ws`);
ws.onmessage = function(event) {
    var receivedData = JSON.parse(event.data);
    if (receivedData.redirect) {
        window.location.href = "/games/" + receivedData.id
    }
    document.getElementById("loading_status").textContent = receivedData.count + "/2";
    document.getElementById("loading_text").textContent = receivedData.text;
};

function sendMessage(event) {
    var messageData = {
        status: 200,
        info: input
    };

    var input = document.getElementById("loading_text")
    // Сериализация JSON-объекта в строку перед отправкой
    ws.send(JSON.stringify(messageData));
    input.value = ''
    event.preventDefault()
}