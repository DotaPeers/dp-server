document.addEventListener('DOMContentLoaded', checkAgentConnectedLoop, false);
var playerId = null;

setInputFilter(document.getElementById("playerIdField"), function(value) {
  return /^\d*$/.test(value); // Allow digits and '.' only, using a RegExp
});


/*
* Restricts input for the given textbox to the given inputFilter function.
*/
function setInputFilter(textbox, inputFilter) {
  ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
    textbox.addEventListener(event, function() {
      if (inputFilter(this.value)) {
        this.oldValue = this.value;
        this.oldSelectionStart = this.selectionStart;
        this.oldSelectionEnd = this.selectionEnd;
      } else if (this.hasOwnProperty("oldValue")) {
        this.value = this.oldValue;
        this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
      } else {
        this.value = "";
      }
    });
  });
}


function formSubmit() {
    $('#playerIdForm').ajaxForm({
        url: "/generate",
        type: 'POST',
        dataType: "json",
        success: function (response) {
            playerId = response["accountId"];
            document.getElementById("pProfilePicture").src = response["picturePath"];
            document.getElementById("pRankImage").src = response["rankPath"];

            document.getElementById("pTextUsername").textContent =    response["username"];
            document.getElementById("pTextAccountId").textContent =   response["accountId"];
            document.getElementById("pTextSteamId").textContent =     response["steamId"];
            document.getElementById("pTextCountryCode").textContent = response["countryCode"];

            document.getElementById("pTextGames").textContent =    response["games"];
            document.getElementById("pTextWins").textContent =     response["wins"];
            document.getElementById("pTextLoses").textContent =    response["loses"];
            document.getElementById("pTextDotaPlus").textContent = response["dotaPlus"];

            document.getElementById("startDownloadBtn").disabled = false;
        },
        error: function (response, a, b, c, d) {
            statusCode = response.status;
            text = response.responseText;

            if (statusCode === 555) {
                alert(text);
            }

        }
    });
}


function startGeneration() {
    $.ajax({
        url: 'generate',
        type: 'POST',
        data: {"startGenerationFor": playerId},
        beforeSend: function () {
            document.getElementById("startDownloadBtn").disabled = true;
            document.getElementById("startDownloadLoader").style.display = "inline-block";
        },
        success: function (response) {
            console.log(response);
            data = JSON.parse(response);

            document.getElementById("startDownloadBtn").disabled = false;
            document.getElementById("startDownloadLoader").style.display = "none";
        },
        error: function (data) {
            console.log("Error" + data);
        }
    });
}


function checkAgentConnectedLoop() {
    checkAgentConnected();
    const interval = setInterval(checkAgentConnected, 2000);
}

/*
*  Checks if the agent is connected.
*  Changes website design depending on the connection status.
*/
function checkAgentConnected() {
    $.ajax({
        url: 'getId',
        type: 'POST',
        data: "agentConnected",
        success: function (data) {
            data = JSON.parse(data);
            imgObj = document.getElementById("userIdImg");
            alertObj = document.getElementById("agentDisconnectedAlert");
            enterBtn = document.getElementById("enterBtn");
            startBtn = document.getElementById("startDownloadBtn");

            if (data["connected"]) {
                imgObj.src = "/static/img/connectedIcon.png";
                imgObj.title = "Agent connected."
                alertObj.style.display = "none";
                enterBtn.disabled = false;
                startBtn.disabled = false;

            } else {
                imgObj.src = "/static/img/notConnectedIcon.png";
                imgObj.title = "Agent not connected."
                alertObj.style.display = "inline-block";
                enterBtn.disabled = true;
                startBtn.disabled = true;
            }
        },
        error: function (data) {
            console.log("Error" + data);
        }
    });
}