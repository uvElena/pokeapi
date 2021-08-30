
$(document).ready(function() {

    $("form").submit(async function(event) {

        event.preventDefault();

        username = $("#usernameinput").val();
        password = $("#inputpassword").val();

        // $.ajax({
        //     type: 'POST',
        //     url: '/api/user/add',
        //     contentType: 'application/json; charset=utf-8',
        //     data: JSON.stringify({username: username, password: password}),
        //     success: function( data ) {
        //         console.log("Success")
        //         console.log(data)
        //     }
        // });

        response = await fetch("/api/user/add", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })

        })
        json_response = await response.json()
        console.log(json_response)

    });
});
