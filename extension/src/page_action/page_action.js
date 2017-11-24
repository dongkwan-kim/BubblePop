/* Make this boolean false for production */
NOW_TEST = false;

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
    addClickListenerToUpdate();
    mediaJSON = sortMediaJSON(mediaJSON, true);
    if (NOW_TEST) {
        addMediaCollection(testMediaJSON);
    } else {
        addMediaCollection(mediaJSON);
    }
});

function getHumanReadableAffinity(n) {
    // TODO more various range
    if (n < 0) {
        return '보수';
    } else {
        return '진보';
    }
}

function getIconFromChecked(checked) {
    return (checked) ? 'check_box' : 'check_box_outline_blank';
}

function getCheckedFromIcon(icon) {
    return (icon == 'check_box');
}

function getCollection(name, icon, affinity, checked) {
    var node = document.createElement("LI");
    node.classList.add("collection-item");
    node.classList.add("avatar");
    node.innerHTML =
        '<img src="' + icon + '" class="circle">'+
        '<span class="title">' + name + '</span>'+
        '<p>' + getHumanReadableAffinity(affinity) + '</p>'+
        '<a href="#!" class="secondary-content">'+
            '<i name="' + name + '" class="material-icons check-icon">'+
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

function addMediaCollection(mediaJSON) {
    var parent = document.getElementById("media-collection");
    mediaJSON = addCheckedToMediaJSON(mediaJSON);
    mediaJSON.map((x) => {
        parent.appendChild(getCollection(x.name, x.icon, x.affinity, x.checked));
    });
}

function addCheckedToMediaJSON(mediaJSON) {
    if (NOW_TEST) {
        var blacklist = ['조선일보'];
    } else {
        // TODO fetch blacklist from server
        var blacklist = [];
    }
    return mediaJSON.map((x) => {
        x.checked = (blacklist.indexOf(x.name) == -1);
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
    var updateJSON = checkList.map((x) => {
        return {
            'name': x.getAttribute('name'),
            'checked': getCheckedFromIcon(x.innerText),
        }
    });
    // TODO send to server;
    console.log(updateJSON);
}

function addClickListenerToUpdate() {
    var btn = document.getElementById("update-btn");
    btn.addEventListener("click", (x) => {
        updateBlackList();
    });
}
