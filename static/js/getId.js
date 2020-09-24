document.addEventListener('DOMContentLoaded', defaultRequestId, false);


function defaultRequestId() {
    requestId(false);
}


function requestId(requestNew) {
    requestType = "default";
    if (requestNew === true) {
        requestType = "new";
    }

    $.ajax({
        url: 'getId',
        type: 'POST',
        data: {"requestId": requestType},
        success: function (data) {
            data = JSON.parse(data);
            document.getElementById("idField").value = data.id;
        },
        error: function (data) {
            console.log("Error" + data);
        }
    });
}