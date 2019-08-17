function follow_async(sourceElem, destElem, follow_username) {
    // $(destElem).html('<img src="{{ url_for('static', filename='loading.gif') }}">');
    $.get("/user/follow_async/"+follow_username
    ).done(function(response) {
        $(destElem).text(response['text'])
    }).fail(function() {
        $(destElem).text("Error: Could not contact server.");
    });
}
