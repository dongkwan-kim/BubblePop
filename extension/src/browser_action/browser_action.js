/* Make this boolean false for production */
var NOW_TEST = false;
var IS_LIBERAL = true;
var API_URL = 'http://localhost:23455';
var BLACK_LIST = [];

var testMediaJSON = [
];

var mediaJSON = [
    {
        "name": "조선일보",
        "affinity": -0.11,
        "rss":"http://www.chosun.com/site/data/rss/politics.xml",
        "icon": "../../icons/조선일보.jpg"
    },
    {
        "name": "중앙일보",
        "affinity": -0.03,
        "rss": "http://rss.joins.com/joins_politics_list.xml",
        "icon": "../../icons/중앙일보.jpg"
    },
    {
        "name": "동아일보",
        "affinity": 0.01,
        "rss": "http://rss.donga.com/politics.xml",
        "icon": "../../icons/동아일보.jpg"
    },
    {
        "name": "매일경제",
        "affinity": 0.14,
        "rss": "http://file.mk.co.kr/news/rss/rss_30200030.xml",
        "icon": "../../icons/매일경제.jpg"
    },
    {
        "name": "한국경제",
        "affinity": -0.19,
        "rss": "http://rss.hankyung.com/new/news_politics.xml",
        "icon": "../../icons/한국경제.png"
    },
    {
        "name": "한겨레신문",
        "affinity": 0.53,
        "rss": "http://www.hani.co.kr/rss/politics/",
        "icon": "../../icons/한겨레신문.jpg"
    },
    {
        "name": "경향신문",
        "affinity": 0.32,
        "rss": "http://www.khan.co.kr/rss/rssdata/politic_news.xml",
        "icon": "../../icons/경향신문.png"
    },
    {
        "name": "오마이뉴스",
        "affinity": 0.42,
        "rss": "http://rss.ohmynews.com/rss/politics.xml",
        "icon": "../../icons/오마이뉴스.png"
    },
    {
        "name": "한국일보",
        "affinity": 0.37,
        "rss": "http://rss.hankooki.com/daily/dh_politics.xml",
        "icon": "../../icons/한국일보.jpg"
    },
    {
        "name": "세계일보",
        "affinity": -0.18,
        "rss": "http://rss.segye.com/segye_politic.xml",
        "icon": "../../icons/세계일보.jpg"
    },
    {
        "name": "국민일보",
        "affinity": 0.18,
        "rss": "http://rss.kmib.co.kr/data/kmibPolRss.xml",
        "icon": "../../icons/국민일보.jpg"
    }
]

document.addEventListener("DOMContentLoaded", function(event) {
    sendToBackground('auth-check', {}, function (msg){
        var is_authenticated = msg.is_authenticated;
        BLACK_LIST = msg.black_list;
        if (is_authenticated) {
            changeVisibleState('auth-body', false);
            /* Give some time to construct */
            setTimeout(function(){
                InitializeMediaCollection();
            }, 100);
        } else {
            changeVisibleState('list-body', false);
            addClickListenerAuth('signin');
            addClickListenerAuth('login');
        }
    })
});

/*
Usage: function sendToBackground("sample", "Hi", function(msg) {
    console.log("message recieved " + msg);
})
*/
function sendToBackground(name, msg, callback) {
    var port = chrome.extension.connect({
        name: name,
    });
    port.postMessage(msg);
    port.onMessage.addListener(callback);
}

function InitializeMediaCollection() {
    /* Add listners */
    addClickListenerToUpdate();
    addClickListenerToSort();

    /* Manipulate MediaJSON */
    mediaJSON = normalizeMediaJSON(mediaJSON);
    mediaJSON = sortMediaJSON(mediaJSON, IS_LIBERAL);

    /* Manipulate DOM */
    if (NOW_TEST) {
        addMediaCollection(testMediaJSON);
    } else {
        addMediaCollection(mediaJSON);
    }
}

function changeVisibleState(className, is_visible) {
    var list_body = document.getElementsByClassName(className)[0];
    var display_style = (is_visible) ? 'block' : 'none';
    list_body.style.display = display_style;
}

function getHumanReadableAffinity(n) {
    var s;
    /* n should be normlized 0 ~ 1 */
    if (n <= 0.25) {
        s = '매우 보수적';
    } else if (n <= 0.5) {
        s = '다소 보수적';
    } else if (n <= 0.75) {
        s = '다소 진보적';
    } else {
        s = '매우 진보적';
    }
    return `${s} (${Math.round(n*100)/100})`;
}

function getIconFromChecked(checked) {
    return (checked) ? 'check_box' : 'check_box_outline_blank';
}

function getCheckedFromIcon(icon) {
    return (icon == 'check_box');
}

function getCollection(mid, name, icon, affinity, checked) {
    var node = document.createElement("LI");
    node.classList.add("collection-item");
    node.classList.add("avatar");
    node.innerHTML =
        '<img src="' + icon + '" class="circle">'+
        '<span class="title">' + name + '</span>'+
        '<p>' + getHumanReadableAffinity(affinity) + '</p>'+
        '<a href="#!" class="secondary-content">'+
            '<i mid="' + mid + '" class="material-icons check-icon">'+
                getIconFromChecked(checked) +
            '</i>'+
        '</a>';
    node.addEventListener("click", (x) => {
        if (x.target.tagName == 'I') {
            updateChecked(x.target);
        }
    });
    return node;
}

function sortMediaJSON(mediaJSON, is_liberal_first) {
    var cpyMediaJSON = JSON.parse(JSON.stringify(mediaJSON));
    var sign = (is_liberal_first) ? -1 : 1;
    return cpyMediaJSON.sort((a, b) => {
        return sign * (a.affinity - b.affinity);
    });
}

function normalizeMediaJSON(mediaJSON) {
    var affinities = mediaJSON.map((x) => {return x.affinity});
    var max_affinity = max(affinities);
    var min_affinity = min(affinities);
    var delta = max_affinity - min_affinity;
    var cpyMediaJSON = JSON.parse(JSON.stringify(mediaJSON));
    return cpyMediaJSON.map((x, i) => {
        x.affinity = (x.affinity - min_affinity) / delta;
        x.id = i;
        return x;
    });
}

function addMediaCollection(mediaJSON) {
    var parent = document.getElementById("media-collection");
    mediaJSON = addCheckedToMediaJSON(mediaJSON);
    mediaJSON.map((x) => {
        parent.appendChild(getCollection(x.id, x.name, x.icon, x.affinity, x.checked));
    });
}

function clearMediaCollection() {
    var parent = document.getElementById("media-collection");
    parent.innerHTML = '';
}

function api_url(url_for_add) {
    return API_URL + url_for_add;
}

function addCheckedToMediaJSON(mediaJSON) {
    return mediaJSON.map((x) => {
        x.checked = (BLACK_LIST.indexOf(x.id) == -1);
        return x;
    });
}

function updateChecked(iconDOM) {
    var current = getCheckedFromIcon(iconDOM.innerText);
    iconDOM.innerText = getIconFromChecked(!current);
}

function updateBlackList() {
    var checkList = document.getElementsByClassName('check-icon');
    checkList = Array.prototype.slice.call(checkList, 0);
    var updateList = checkList.filter((x) => {
        var id = parseInt(x.getAttribute('mid'));
        var checked_before = BLACK_LIST.indexOf(id) == -1;
        var checked = getCheckedFromIcon(x.innerText);
        return checked_before != checked;
    }).map((x) => {
        return parseInt(x.getAttribute('mid'));
    });

    sendToBackground("update-black-list", {
        update_list: updateList,
    }, function (res) { /* Do nothing */ })
}

function addClickListenerToUpdate() {
    var btn = document.getElementById("update-btn");
    btn.addEventListener("click", (x) => {
        updateBlackList();
    });
}

function toggleSortingMedia() {
    IS_LIBERAL = !IS_LIBERAL;
    mediaJSON = sortMediaJSON(mediaJSON, IS_LIBERAL);
    clearMediaCollection();
    addMediaCollection(mediaJSON);
}

function addClickListenerToSort() {
    var btn = document.getElementById("sort-btn");

    /* Initialize */
    var label = document.getElementById("sort-label");
    label.innerText = (IS_LIBERAL) ? '진보적인 순' : '보수적인 순';

    btn.addEventListener("click", (x) => {
        toggleSortingMedia();
        label.innerText = (IS_LIBERAL) ? '진보적인 순' : '보수적인 순';
    });
}

function addClickListenerAuth(type) {
    var btn_id = (type == 'signin') ? 'signin-btn' : 'login-btn';
    var btn = document.getElementById(btn_id);

    btn.addEventListener("click", (x) => {
        var user_id = document.getElementById('user-id');
        var user_password = document.getElementById('user-password');
        var type = x.target.id.split('-')[0];
        var req = {
            "type": type,
            "user_id": user_id.value,
            "user_password": user_password.value,
        }
        sendToBackground("auth-event", req, function (res){
            if (res.is_authenticated) {
                BLACK_LIST = res.black_list;
                changeVisibleState('auth-body', false);
                changeVisibleState('list-body', true);
                InitializeMediaCollection();
            }
        })
    });
}


/* Statistics from https://simplestatistics.org/ (ISC License) */

function max(x) {
    var value = x[0];
    for (var i = 1; i < x.length; i++) {
        if (x[i] > value) {
            value = x[i];
        }
    }
    return value;
}

function min(x) {
    var value = x[0];
    for (var i = 1; i < x.length; i++) {
        if (x[i] < value) {
            value = x[i];
        }
    }
    return value;
}
