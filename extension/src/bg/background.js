/* Gloabal */
var IS_AUTHENTICATED = false;
var TOKEN = '';
var API_URL = 'http://13.124.151.77:23455';

function api_url(url_for_add) {
    return API_URL + url_for_add;
}

chrome.extension.onConnect.addListener(function(port) {
    if (port.name == 'auth-event') {
        port.onMessage.addListener(function(msg) {
            var type = msg.type;
            var user_id = msg.user_id;
            var user_password = msg.user_password;

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
                        if (!result.result)
                            return;
                        result.black_list = [];
                        TOKEN = result.token;
                        IS_AUTHENTICATED = true;
                        result.is_authenticated = true;
                        port.postMessage(result);
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
                        if (!result.result)
                            return;
                        TOKEN = result.token;
                        IS_AUTHENTICATED = true;
                        result.is_authenticated = true;
                        port.postMessage(result);
                    }
                });
            }
        });
    } else if (port.name == 'auth-check') {
        port.onMessage.addListener(function(res) {
            if (IS_AUTHENTICATED) {
                $.ajax({
                    url: api_url("/api/blacklist/"),
                    type: 'POST',
                    data: {
                        token: TOKEN,
                    },
                    success: function(result){
                        port.postMessage({
                            is_authenticated: IS_AUTHENTICATED,
                            black_list: result.black_list,
                        });
                    }
                });
            } else {
                port.postMessage({
                    is_authenticated: IS_AUTHENTICATED,
                    black_list: [],
                });
            }
        });
    } else if (port.name == 'update-black-list') {
        port.onMessage.addListener(function(res) {
            var update_list = res.update_list;
            $.ajax({
                url: api_url("/api/change/"),
                type: 'POST',
                data: {
                    token: TOKEN,
                    media: update_list,
                },
                success: function(result){
                    port.postMessage(result);
                }
            });
        });
    }
})

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request.type == 'fetch-ssdv') {
            var article_url = request.article_url;
            $.ajax({
                url: api_url('/api/articles/'),
                type: 'POST',
                data: {
                    token: TOKEN,
                    url: article_url,
                },
                success: sendResponse,
            });
        } else if (request.type == 'error-report') {
            var url_a = request.url_a;
            var url_b = request.url_b;
            $.ajax({
                url: api_url('/api/report/'),
                type: 'POST',
                data: {
                    token: TOKEN,
                    url_a: url_a,
                    url_b: url_b,
                    content: '',
                },
                success: sendResponse,
            });
        } else if (request.type == 'check-url') {
            var article_url = request.article_url;
            console.log(article_url);
            $.ajax({
                url: api_url('/api/check/'),
                type: 'POST',
                data: {
                    token: TOKEN,
                    url: article_url,
                },
                success: sendResponse,
            });
        }
        return true;
    }
);
