/* Make this boolean false for production */
NOW_TEST = true;

var testMediaJSON = [
    {
        "name": "조선일보",
        "affinity": -1,
        "icon": ""
    },
    {
        "name": "한겨레신문",
        "affinity": 1,
        "icon": ""
    },
    {
        "name": "조선일보",
        "affinity": -1,
        "icon": ""
    },
    {
        "name": "한겨레신문",
        "affinity": 1,
        "icon": ""
    },
];

var mediaJSON = [
];

document.addEventListener("DOMContentLoaded", function(event) {
    addClickListenerToUpdate();
    if (NOW_TEST) {
        addMediaCollection(testMediaJSON);
    } else {
        // TODO
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
