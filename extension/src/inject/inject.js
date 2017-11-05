chrome.extension.sendMessage({}, function(response) {
    var readyStateCheckInterval = setInterval(function() {
        if (document.readyState === "complete") {
            clearInterval(readyStateCheckInterval);

            // This part of the script triggers when page is done loading
            console.log("Hello. This message was sent from scripts/inject.js");
            parseFeedPeriod(1500);
        }
    }, 10);
});

/* Perodically, parse NewsFeed,
 * because users can load their feed dynamically */
function parseFeedPeriod(period) {

    var state = { oldFeed: 0, newFeed: 0 };

    setInterval(function(){
        var linkList = getLinkList();
        state.newFeed = linkList.length;

        /* If feed has been changed, parse again. */
        if(state.oldFeed != state.newFeed) {
            for(var i = 0; i < linkList.length; i++) {
                linkDOM = linkList[i];
                realLink = getRealLink(linkDOM.href);
                if(isServiceable(realLink)){
                    appendSSDVBtn(linkList[i], realLink);
                }
            }
            state.oldFeed = state.newFeed;
        }
    }, period);
}

/* If system can give SSDV list of the given link, return true. */
function isServiceable(link) {
    // TODO: implementation w/ Ajax
    return true;
}

function appendSSDVBtn(linkDOM, link) {
    var injectDOM = getAncestor(linkDOM, 8);

    /* If there's already SSDVBtn, do not add again. */
    if(hasClass(injectDOM, "SSDV-added")){
        return;
    }
    injectDOM.classList.add("SSDV-added")

    var node = document.createElement("DIV");
    node.classList.add("request-ssdv-btn");
    node.setAttribute("data", link);
    var textnode = document.createTextNode("+");
    node.appendChild(textnode);

    injectDOM.appendChild(node);
    console.log(node);
}

function getAncestor(dom, num) {
    var tmp = dom;
    for(var idx = 0; idx < num; idx++) {
        tmp = tmp.parentNode;
    }
    return tmp;
}

function getLinkList() {
    linkClass = "_52c6"
    linkList = document.getElementsByClassName(linkClass);
    return linkList;
}

function getRealLink(target) {
    if(target.includes("https://l.facebook.com")) {
        return parseURL(target, "u");
    } else {
        return target;
    }
}

function parseURL(url, variable) {
    var query = url.split("?")[1];
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
    return null;
}

/* https://stackoverflow.com/a/15226442 */
function hasClass(target, className) {
    return new RegExp('(\\s|^)' + className + '(\\s|$)').test(target.className);
}
