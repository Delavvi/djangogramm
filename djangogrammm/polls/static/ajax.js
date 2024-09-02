$(document).on('submit', ".product-form", function (e) {
    var form = $(this);
    console.log('submit button clicked successfully');
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            if (data.hasOwnProperty('likes')) {
                var postID = form.find('button[name="post_id_like"]').val();
                var likeCountElement = $('#like-count-' + postID);
                var dislikeCountElement = $('#dislike-count-' + postID);
                likeCountElement.text(data.likes);
                dislikeCountElement.text(data.dislikes);
            }
        },
        error: function () {
            console.log('ERROR with ajax request');
        },
    });
    e.preventDefault();
});


$(document).on('submit', ".dislike-form", function (e) {
            var form = $(this);
            console.log(
                'submit button clicked successfully');

            $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                dataType: 'json',
                data: {
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function (data) {
                        if (data.hasOwnProperty('dislikes')) {
                            var postID = form.find('button[name="post_id_dislike"]').val();
                            var likeCountElement = $('#like-count-' + postID);
                            var dislikeCountElement = $('#dislike-count-' + postID);

                            dislikeCountElement.text(data.dislikes);
                            likeCountElement.text(data.likes);

                    }
                },
                error: function (){
                    console.log('ERROR with ajax request');
                },
            });
            e.preventDefault();
        });



$(document).on('submit', ".like", function (e) {
            var form = $(this);
            console.log(
                'submit button clicked successfully');

            $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                dataType: 'json',
                data: {
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function (data) {
                        var postID = form.find('button[name="post_id_like"]').val();
                        var likeCountElement = $('#like-count-' + postID);
                        likeCountElement.text(data.likes);
                        var dislikeCountElement = $('#dislike-count-' + postID);
                        dislikeCountElement.text(data.dislikes);

                },
                error: function (){
                    console.log('ERROR with ajax request');
                },
            });
            e.preventDefault();
        });


$(document).on('submit', ".dislike-newsform", function (e) {
            var form = $(this);
            console.log(
                'submit button clicked successfully');

            $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                dataType: 'json',
                data: {
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function (data) {
                        var postID = form.find('button[name="post_id_dislike"]').val();
                        var dislikeCountElement = $('#dislike-count-' + postID);
                        var likeCountElement = $('#like-count-' + postID);
                        dislikeCountElement.text(data.dislikes);
                        likeCountElement.text(data.likes);
                },
                error: function (){
                    console.log('ERROR with ajax request');
                },
            });
            e.preventDefault();
        });

$(document).on('submit', ".subscribe-form", function (e) {
    var form = $(this);
    console.log('Submit button clicked successfully');

    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            console.log('Success response:', data)
            var subscribeButton = form.find('button[name="subscribe_button"]');
            if(data.subscribe_status === false){
                subscribeButton.text('Unsubscribe');
            }
            else if(data.subscribe_status === true){
                subscribeButton.text('Subscribe');
            }
        },
        error: function (xhr, status, error) {
            console.log('Error with AJAX request:', error);
        },
    });
    e.preventDefault();
});




$(document).on('submit', ".tags-form", function (e) {
    var form = $(this);
    console.log('Submit button clicked successfully');

    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            new_tags: form.find('input[name=new_tags]').val()
        },
        success: function (data) {
    console.log('Success response:', data);
            var tagsContainer = $('div[id="tags-container' + form.find('button').val() + '"]');
            var updatedTags = data.tags;
            updatedTags.forEach(function(tag) {
                tagsContainer.append(' ');
                var tagElement = $('<small>').text(tag);
                tagsContainer.append(tagElement);
            });
        },
        error: function (xhr, status, error) {
            console.log('Error with AJAX request:', error);
        },
    });
    e.preventDefault();
});


$(document).on('submit', ".user_info_form", function (e) {
    var form = $(this);
    console.log('Submit button clicked successfully');

    $.ajax({
        type: 'GET',
        url: form.attr('action'),
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            var modalId = '#UserDataOne' + form.find('button').val();
            var modal = $(modalId);
            modal.find('img').attr('src', data.avatar);
            modal.find('h2').text(data.name);
            modal.find('p').text(data.bio);
        },
        error: function (xhr, status, error) {
            console.log('Error with AJAX request:', error);
        },
    });
    e.preventDefault();
});


$(document).on('click', ".user_info_form button[type='submit']", function (e) {
    var form = $(this).closest('.user_info_form');
    console.log('Submit button clicked successfully');

    $.ajax({
        type: 'GET',
        url: form.attr('action'),
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            var modalId = '#PostData' + form.find('button').val();
            var modal = $(modalId);
            modal.find('img').attr('src', data.avatar);
            modal.find('h2').text(data.name);
            modal.find('p').text(data.bio);
        },
        error: function (xhr, status, error) {
            console.log('Error with AJAX request:', error);
        },
    });
    e.preventDefault();
});