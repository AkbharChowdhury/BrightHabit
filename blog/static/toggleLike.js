  $(document).ready(function () {
    $("#like_toggle_form").submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: $('#url').val(),
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                post_id: $('#post_id').val()
            },
            success: (data) => {
                $('#total_likes').text(data.total_likes)
                $('#like_icon').prop('class', `${data.liked_icon} fa-heart fa-lg`)
            },
            error: (e) => console.error(`There was an error with handling this request ${e.message}`)

        });
    });
});