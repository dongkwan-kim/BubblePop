/* Gloabal */
var IS_AUTHENTICATED = false;
var API_URL = 'http://13.124.151.77:8080';

function api_url(url_for_add) {
    return API_URL + url_for_add;
}

function fetch_black_list() {
    if (IS_AUTHENTICATED) {
        // TODO ajax
        return [0];
    } else {
        return [];
    }
}

function update_black_list(port, lst) {
    // TODO ajax and send response to port;
}

chrome.extension.onConnect.addListener(function(port) {
    if (port.name == 'auth-event') {
        port.onMessage.addListener(function(msg) {
            var type = msg.type;
            var user_id = msg.user_id;
            var user_password = msg.user_password;
            var is_authenticated;

            /* TODO auth */
            if (type == 'signin') {
                $.ajax({
                    url: api_url("/session/register"),
                    type: 'POST',
                    data: {
                        username: user_id,
                        password: user_password,
                        password_check: user_password,
                    },
                    success: function(result){
                        console.log(result)
                    }
                });
            } else if (type == 'login') {
                $.ajax({
                    url: api_url("/session/login"),
                    type: 'POST',
                    data: {
                        username: user_id,
                        password: user_password,
                    },
                    success: function(result){
                        console.log(result)
                    }
                });
            }
            is_authenticated = true;
            IS_AUTHENTICATED = is_authenticated;

            var res = {};
            res.user_id = user_id;
            res.black_list = fetch_black_list();
            res.is_authenticated = is_authenticated;

            port.postMessage(res);
        });
    } else if (port.name == 'auth-check') {
        port.onMessage.addListener(function(res) {
            port.postMessage({
                is_authenticated: IS_AUTHENTICATED,
                black_list: fetch_black_list(),
            });
        });
    } else if (port.name == 'update-black-list') {
        port.onMessage.addListener(function(res) {
            update_black_list(port, res.update_list);
        });
    }
})

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request.type == 'fetch-ssdv') {
            var article_url = request.article_url;
            $.ajax({
                url: api_url(`/api/articles/?url=${article_url}`),
                type: 'GET',
                success: function(result){
                    sendResponse({
                        result: result,
                    });
                }
            });
        }
    }
);
