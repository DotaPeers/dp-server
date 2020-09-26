
/*
* Function for the "Start Graph Generation" Button
*/
function startGraphGeneration(playerId) {
    $.ajax({
        url: 'create',
        type: 'POST',
        data: "startCreation",
        beforeSend: function () {
            document.getElementById("startGenLoader").style.display = "inline-block";
        },
        success: function (response) {
            data = JSON.parse(response);

            document.getElementById("startGenLoader").style.display = "none";

            if (data['status'] === 'OK') {
                window.location.href = '/graph/' + playerId;
            }
        },
        error: function (data) {
            console.log("Error" + data);

            document.getElementById("startGenLoader").style.display = "none";
        }
    });
}
