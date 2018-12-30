    if(typeof(String.prototype.trim) === "undefined")
    {
        String.prototype.trim = function()
        {
            return String(this).replace(/^\s+|\s+$/g, '');
        };
    }

    function api_call(input) {
        $.ajax({
            url: "http://0.0.0.0:5000/api",
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(input),

            success: function (data, textStatus, jQxhr) {
                console.log(data)
                $('.little-squre-box h3').html( data.score );
            },
            error(jqXHR, textStatus, errorThrown) {
                console.log(errorThrown);
            },
            timeout: 30000 // sets timeout to 10 seconds
        });

    }


    $(document).ready(function () {
        // request when clicking on the button
        $('#submit').click(function () {
            // get the input data
            var raw_text = $('#mytextarea').val();
            var type = $('#btn-essay-type .active input').val();
            var level = $('#btn-grade-level .active input').val();
            var score_range = $('#btn-score-range .active input').val();

            input = {'raw_text': raw_text, 'type': type, 'level': level, 'score_range': score_range}
            console.log(input);
            api_call(input);
        });

    });

