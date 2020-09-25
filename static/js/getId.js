document.addEventListener('DOMContentLoaded', defaultRequestId, false);
document.addEventListener('DOMContentLoaded', checkAgentConnectedLoop, false);


function defaultRequestId() {
    requestId(false);
}


/*
*  Requests a (new) ID for the user.
*/
function requestId(requestNew) {
    requestType = "default";
    if (requestNew === true) {
        requestType = "new";
    }

    $.ajax({
        url: 'getId',
        type: 'POST',
        data: {"requestId": requestType},
        beforeSend: function () {
            clearAgentConnected();
        },
        success: function (data) {
            data = JSON.parse(data);
            document.getElementById("idField").value = data.id;
            document.getElementById("userIdSpan").textContent = data.id;
            document.getElementById("userIdDiv").classList.remove("invisible");
        },
        error: function (data) {
            console.log("Error" + data);
        }
    });
}

/*
*  Clears the agent connected status. This resets the next button and the other indicators
*/
function clearAgentConnected() {
    imgObj = document.getElementById("userIdImg");
    textObj = document.getElementById("agentConnected");
    textObj.classList.remove("text-primary");
    textObj.classList.remove("text-success");
    btnObj = document.getElementById("nextBtn");

    textObj.textContent = "False";
    textObj.classList.add("text-primary");
    imgObj.src = "/static/img/notConnectedIcon.png";
    imgObj.title = "Agent not connected."
    btnObj.disabled = true;
}


function checkAgentConnectedLoop() {
    const interval = setInterval(checkAgentConnected, 2000);
}

/*
*  Checks if the agent is connected.
*/
function checkAgentConnected() {
    $.ajax({
        url: 'getId',
        type: 'POST',
        data: "agentConnected",
        success: function (data) {
            data = JSON.parse(data);
            imgObj = document.getElementById("userIdImg");
            textObj = document.getElementById("agentConnected");
            textObj.classList.remove("text-primary");
            textObj.classList.remove("text-success");
            btnObj = document.getElementById("nextBtn");

            if (data["connected"]) {
                imgObj.src = "/static/img/connectedIcon.png";
                imgObj.title = "Agent connected."
                textObj.textContent = "True";
                textObj.classList.add("text-success");
                btnObj.disabled = false;

            } else {
                imgObj.src = "/static/img/notConnectedIcon.png";
                imgObj.title = "Agent not connected."
                textObj.textContent = "False";
                textObj.classList.add("text-primary");
                btnObj.disabled = true;

            }
        },
        error: function (data) {
            console.log("Error" + data);
        }
    });
}
