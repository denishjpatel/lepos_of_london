function myFunction(id) {
    var csrfmiddlewaretoken = $("[name='csrfmiddlewaretoken']").val();

    $.ajax({
        method: "POST",
        url: "/add_wishlist/",
        data: { "id": id, csrfmiddlewaretoken: csrfmiddlewaretoken },
        success: function(response) {
            alertify.set('notifier', 'position', 'top-right');
            if (response.success) {
                alertify.success(response.success);
            } else {
                alertify.error(response.error);
            }

        }
    });

};