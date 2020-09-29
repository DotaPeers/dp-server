
/*
*  This function gets called on every page and changes the default behaviour of the alert close button to hide the alert
*  instead of destroying it. Why would you do this in the first place anyways...
*/
$(function(){
    $(".close").on("click", function(){
        $(this).closest(".alert").css("display", "none");
    })
})
