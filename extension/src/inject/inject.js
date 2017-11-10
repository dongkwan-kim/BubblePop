chrome.extension.sendMessage({}, function(response) {
    var readyStateCheckInterval = setInterval(function() {
        if (document.readyState === "complete") {
            clearInterval(readyStateCheckInterval);

            // This part of the script triggers when page is done loading
            console.log("Hello. This message was sent from scripts/inject.js");

            var modalId = "ssdv-modal";
            var modal = createModalWindow(modalId);
            parseFeedPeriod(1500, modal);
        }
    }, 10);
});

/* Perodically, parse NewsFeed,
 * because users can load their feed dynamically */
function parseFeedPeriod(period, ssdvModal) {

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
                    appendSSDVBtn(linkList[i], realLink, ssdvModal);
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

function appendSSDVBtn(linkDOM, link, ssdvModal) {
    var injectDOM = getAncestor(linkDOM, 8);

    /* If there's already SSDVBtn, do not add again. */
    if(hasClass(injectDOM, "SSDV-added")
        || hasClass(linkDOM, "SSDV-no-need")){
        return;
    }
    injectDOM.classList.add("SSDV-added")

    var node = document.createElement("DIV");
    node.classList.add("request-ssdv-btn");
    node.setAttribute("data", link);
    node.addEventListener("click", () => {modalHandler(ssdvModal);});

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

/* Modal */
function createModalWindow(modalId) {
    var child = document.createElement('div');
    child.className = "inside";
    child.id = modalId;

    var header = document.createElement('h1');
    header.className = "modal-header";
    child.appendChild(header);

    var body = document.createElement("div");
    body.className = "modal-body";
    child.appendChild(body);

    return new Modal(child, false);
}

function modalHandler(ssdvModal) {
    var c = ssdvModal.child;
    var modalHeader = c.getElementsByClassName("modal-header")[0];
    var modalBody = c.getElementsByClassName("modal-body")[0];
    var ea = testEmbeddedArticle();
    modalBody.innerHTML = ea;
    modalHeader.innerHTML = '다른 시각의 뉴스';
    ssdvModal.show();
}

function embeddedArticle(url, thumbnail, title, description, media) {
    var template =
    '<div class="embedded-article _6m2 _1zpr clearfix _dcs _4_w4 _59ap _5qqr" data-ft="{&quot;tn&quot;:&quot;H&quot;}">'+
        '<div class="clearfix _2r3x">'+
            '<div class="lfloat _ohe">'+
                '<span class="_3m6-">'+
                    '<div class="_6ks">'+
                        '<a href="' + url + '" tabindex="-1" target="_blank">'+
                            '<div class="_6l- __c_">'+
                                '<div class="uiScaledImageContainer fbStoryAttachmentImage" style="max-width:474px;max-height:247px;">'+
                                    '<img class="scaledImageFitWidth img" src="' + thumbnail + ' style="top:0px;" alt="" width="474" height="248">'+
                                '</div>'+
                            '</div>'+
                        '</a>'+
                    '</div>'+
                    '<div class="_3ekx _29_4"><div class="_6m3 _--6">'+
                        '<div class="mbs _6m6 _2cnj _5s6c">'+
                            '<a href="' + url + '" target="_blank">' + title + '</a>'+
                        '</div>'+
                        '<div class="_6m7 _3bt9">' + description + '</div>'+
                        '<div class="_59tj _2iau"><div class="_6lz _6mb ellipsis">' + media + '</div></div>'+
                    '</div>'+
                    '<a class="_52c6 SSDV-no-need" href="' + url + '" tabindex="-1" target="_blank"></a>'+
                    '</div>'+
                '</span>'+
            '</div>'+
            '<div class="_42ef"><span class="_3c21"></span></div>'+
        '</div>'+
    '</div>'
    return template;
}

function testEmbeddedArticle() {
    return embeddedArticle(
        "http://news.chosun.com/site/data/html_dir/2017/11/11/2017111100920.html?Dep0=facebook&topics",
        "https://external.ficn2-1.fna.fbcdn.net/safe_image.php?d=AQAsZZZ0CtUXdOgv&w=476&h=249&url=http%3A%2F%2Fimage.chosun.com%2Fsitedata%2Fimage%2F201711%2F11%2F2017111100884_0.jpg&cfs=1&upscale=1&fallback=news_d_placeholder_publisher&_nc_hash=AQDSTO4vPjj7uJ54",
        '20대 10명中 7명 "빼빼로데이 비용 부담 돼"',
        "20대 10명 중 7명은 빼빼로데이를 챙기는 것에 부담을 느끼는 것으로 조사됐다. 구인사이트 알바천국이 10월 27일부터 지난 9일까지 20대 ..",
        "조선일보",
    );
}
