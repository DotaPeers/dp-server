document.addEventListener('DOMContentLoaded', checkAgentConnectedLoop, false);
var playerId = null;
var agentConnected = false;
var isDownloading = false;


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

/*
*  Checks if all conditions are set for the "Enter" button to be enabled.
*/
function validateEnterBtn() {
    enterBtn = document.getElementById("enterBtn");

    if (agentConnected) {
        enterBtn.disabled = false;
    } else {
        enterBtn.disabled = true;
    }
}

/*
* Checks if all conditions are set for the "StartDownload" button to be enabled.
*/
function validateStartBtn() {
    startBtn = document.getElementById("startDownloadBtn");

    if (agentConnected && playerId && !isDownloading) {
        startBtn.disabled = false;
    } else {
        startBtn.disabled = true;
    }
}


function formSubmit() {
    $('#playerIdForm').ajaxForm({
        url: "/generate",
        type: 'POST',
        dataType: "json",
        success: function (response) {
            status = response['status'];

            if (status === "OK") {
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

                validateStartBtn();

                document.getElementById("invalidIdAlert").style.display = "none";
                document.getElementById("playerNotExistAlert").style.display = "none";

            } else if (status === 'INVALID_ID') {
                document.getElementById("invalidIdAlert").style.display = "inline-block";

            } else if (status === 'PLAYER_NOT_EXISTING') {
                document.getElementById("playerNotExistAlert").style.display = "inline-block";
            }

        },
        error: function (response) {
            console.log("Error: " + response);
        }
    });
}


function startGeneration() {
    $.ajax({
        url: 'generate',
        type: 'POST',
        data: {"startGenerationFor": playerId},
        beforeSend: function () {
            isDownloading = true;
            validateStartBtn();
            document.getElementById("startDownloadLoader").style.display = "inline-block";
            document.getElementById("downloadInProgressAlert").style.display = "inline-block";
        },
        success: function (response) {
            data = JSON.parse(response);

            isDownloading = false;
            validateStartBtn();
            document.getElementById("startDownloadLoader").style.display = "none";
            document.getElementById("downloadInProgressAlert").style.display = "none";
        },
        error: function (data) {
            console.log("Error" + data);

            isDownloading = false;
            validateStartBtn();
            document.getElementById("startDownloadLoader").style.display = "none";
            document.getElementById("downloadInProgressAlert").style.display = "none";
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

            if (data["connected"]) {
                agentConnected = true;
                imgObj.src = "/static/img/connectedIcon.png";
                imgObj.title = "Agent connected."
                alertObj.style.display = "none";

            } else {
                agentConnected = false;
                imgObj.src = "/static/img/notConnectedIcon.png";
                imgObj.title = "Agent not connected."
                alertObj.style.display = "inline-block";
            }

            validateEnterBtn();
            validateStartBtn();
        },
        error: function (data) {
            console.log("Error" + data);
        }
    });
}
