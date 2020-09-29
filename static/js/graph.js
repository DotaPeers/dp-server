setInputFilter(document.getElementById("playerIdField"), function(value) {
  return /^\d*$/.test(value); // Allow digits and '.' only, using a RegExp
});

/*
*  Enters the Player Id
*/
function formSubmit() {
    $('#playerIdForm').ajaxForm({
        url: "/graph",
        type: 'POST',
        dataType: "json",
        success: function (data, a, b, c) {
            console.log(data);
            console.log(a);
            console.log(b);
            console.log(c);
            if (data["status"] === "OK") {
                document.getElementById("invalidIdAlert").style.display = "none";
                playerId = document.getElementById("playerIdField").value;
                window.location.href = '/graph/' + playerId;

            } else {
                document.getElementById("invalidIdAlert").style.display = "inline-block";
            }
        },
        error: function (data) {
            console.log("Error" + data);
            console.log(data);
            document.getElementById("invalidIdAlert").style.display = "none";
        }
    });
}
