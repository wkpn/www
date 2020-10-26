let form = $("#send_telegram_message");

form.submit(function(e) {
    e.preventDefault();

    $.ajax({
        type: "POST",
        url: "/telegram/form",
        data: form.serialize(),

        success: function(response) {
            alert(response);
            form.trigger("reset");
        }
    });
});