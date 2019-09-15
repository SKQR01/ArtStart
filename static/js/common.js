
$(document).ready(function () {
    $("#likeButton").click(function () {
        $.ajax({
            type: "GET",
            url: location.href + '/add_like',
            success: function (data) {
                $("#h3").html(data);
            }
        });
        return false;
    });
});

$("#comment_form").submit(function () {


    let str = document.getElementById("comment_text").value;

    $.ajax({
        type: "GET",
        url: location.href + '/add_comment',
        data: {
            "text":str
        },
        success: function (data) {
            $("#comments").append("<div>" + data + "</div>");
        }
    });
    return false;
});