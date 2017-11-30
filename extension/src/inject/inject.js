var API_URL = 'http://13.124.151.77:23455';
var MEDIA_LIST = ['조선일보', '중앙일보', '동아일보', '매일경제', '국민일보',
    '경향신문', '한국일보', '오마이뉴스', '한겨레신문'];

function api_url(url_for_add) {
    return API_URL + url_for_add;
}

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
                var linkDOM = linkList[i];
                realLink = getRealLink(linkDOM.href);
                appendSSDVBtnServiceable(linkDOM, realLink, ssdvModal, appendSSDVBtn);
            }
            state.oldFeed = state.newFeed;
        }
    }, period);
}

/* If system can give SSDV list of the given link, run callback */
function appendSSDVBtnServiceable(linkDOM, realLink, ssdvModal, callback) {

    /* If it is already inspected or it is from Modal,
       do not add SSDVBtn. */
    if(hasClass(linkDOM, "SSDV-marked")
        || hasClass(linkDOM, "SSDV-no-need")){
        return;
    }

    linkDOM.classList.add("SSDV-marked");

    chrome.runtime.sendMessage({
        type: 'check-url',
        article_url: realLink,
    }, function (response) {
        if (response.result) {
            callback(linkDOM, realLink, ssdvModal);
        }
    });
}

function appendSSDVBtn(linkDOM, link, ssdvModal) {
    var injectDOM = getAncestor(linkDOM, 8);

    /* If there's already SSDVBtn or it is from Modal,
       do not add SSDVBtn. */
    if(hasClass(injectDOM, "SSDV-added")
        || hasClass(linkDOM, "SSDV-no-need")){
        return;
    }

    injectDOM.classList.add("SSDV-added")

    var node = document.createElement("DIV");
    node.classList.add("request-ssdv-btn");
    node.setAttribute("data", link);
    node.addEventListener("click", () => {modalHandler(ssdvModal, link);});

    var textnode = document.createTextNode("+");
    node.appendChild(textnode);

    injectDOM.appendChild(node);
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

    var graph = document.createElement('div');
    graph.className = 'modal-graph';
    child.appendChild(graph);

    var body = document.createElement("div");
    body.className = "modal-body";
    body.style.height = window.outerHeight * 0.5 + 'px';
    child.appendChild(body);

    return new Modal(child, false);
}

function updateAffinityGraph(graphSelector, newsNumberList, categories) {
    if (categories.length != newsNumberList.length) {
        console.log("catetories and newsNumberList are not matched.");
        return false;
    }
    newsNumberList.unshift('#기사');
    colorList = getColorGradientList(categories.length, 'red', 'blue');
    bb.generate({
        bindto: graphSelector,
        size: {
            height: 70
        },
        axis: {
            "x": {
                "type": "category",
                "categories": categories
            },
            y: {
                show: false
            }
        },
        legend: {
            show: false,
        },
        data: {
            columns: [
                newsNumberList,
            ],
            types: {
                '#기사': "bar",
            },
            color: function (color, d) {
                if (Number.isInteger(d.index)){
                    return colorList[d.index];
                } else{
                    return "white"
                }
            }
        },
    });
}

function getColorGradientList(numberOfItems, start, end) {
    var rainbow = new Rainbow();
    rainbow.setNumberRange(1, numberOfItems);
    rainbow.setSpectrum(start, end);
    var r = [];
    for (var i = 1; i <= numberOfItems; i++) {
        var hexColour = rainbow.colourAt(i);
        r.push('#' + hexColour);
    }
    return r;
}

function modalHandler(ssdvModal, link) {
    var c = ssdvModal.child;
    var modalHeader = c.getElementsByClassName("modal-header")[0];
    modalHeader.innerHTML = '다른 시각의 뉴스';

    var modalBody = c.getElementsByClassName("modal-body")[0];

    /* fetchSSDVFromBackground */
    chrome.runtime.sendMessage({
        type: 'fetch-ssdv',
        article_url: link,
    }, function (response) {

        if (!response.success) {
            /* Unauthorized */
            if (response.status == 401) {
                alert("로그인이 필요합니다. 탭 오른쪽에서 'BubblePop' 아이콘을 클릭해주세요!");
            } else {
                console.log(response);
            }
            return;
        }

        var lst = response.article_list;
        var user_media_list = MEDIA_LIST.filter((x) => {
            return response.black_list.indexOf(x) == -1;
        })
        var html = '';
        var media_count = user_media_list.map(() => {return 0});
        for (var i = 0; i < lst.length; i++) {
            html += embeddedArticle(lst[i].url, lst[i].title,
                lst[i].description, lst[i].media_name, api_url(lst[i].media_icon));
            media_count[user_media_list.indexOf(lst[i].media_name)] += 1;
        }
        modalBody.innerHTML = html;

        /* Error report */
        var report_btns = modalBody.getElementsByClassName('report-btn');
        report_btns = Array.prototype.slice.call(report_btns, 0);
        report_btns.map((x) => {
            x.addEventListener('click', (e) => {
                var data = e.target.getAttribute('data');
                chrome.runtime.sendMessage({
                    type: 'error-report',
                    url_a: link,
                    url_b: data,
                }, function (response) {
                    alert('신고되었습니다. 감사합니다.')
                })
            })
        });

        ssdvModal.show();
        updateAffinityGraph('.modal-graph', media_count, user_media_list);
    });
}

function embeddedArticle(url, title, description, media, icon) {
    var template =
    '<div class="row article">'+
        '<div class="embedded-title col s2">'+
            `<img class="circle" src="${icon}">`+
            `<div class="media-title">${media}</div>`+
            `<div><a data="${url}" class="report-btn">오류 신고</a></div>`+
        '</div>'+
        '<div class="embedded-article col s10 _6m2 _1zpr clearfix _dcs _4_w4 _59ap _5qqr" data-ft="{&quot;tn&quot;:&quot;H&quot;}">'+
            '<div class="clearfix _2r3x">'+
                '<div class="lfloat _ohe">'+
                    '<span class="_3m6-">'+
                        '<div class="_3ekx _29_4"><div class="_6m3 _--6 my_6m3">'+
                            '<div class="mbs _6m6 _2cnj _5s6c my_5s6c">'+
                                `<a href="${url}" target="_blank">${title}</a>`+
                            '</div>'+
                            `<div class="_3bt9 my_3bt9">${description}</div>`+
                        '</div>'+
                        `<a class="_52c6 SSDV-no-need" href="${url}" tabindex="-1" target="_blank"></a>`+
                        '</div>'+
                    '</span>'+
                '</div>'+
            '</div>'+
        '</div>'+
    '</div>'
    return template;
}
