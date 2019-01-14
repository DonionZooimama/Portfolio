
chrome.storage.local.get('channel', function (result) {
    if(result.channel){ 
        document.getElementById("AddChannel").value = result.channel;
    }
});

document.getElementById("AddChannel").addEventListener("change", add);
document.getElementById("RemoveChannel").addEventListener("change", remove_channel);
document.getElementById("Add").addEventListener("click", add);
document.getElementById("Remove").addEventListener("click", remove_channel);

document.getElementById("Speed").addEventListener("input", set_playback_speed);

document.getElementById("RemoveAll").addEventListener("click", remove_all);
if (document.getElementById("myonoffswitch")){
    document.getElementById("myonoffswitch").addEventListener("click", disable);
}

if (document.getElementById("Disable_Recommended")){
    document.getElementById("Disable_Recommended").addEventListener("click", disable_recommendations);
}

document.getElementById("Pay").addEventListener("click", function(){chrome.tabs.create({"url": "donate.html"});});

chrome.storage.local.get('recommended', function (result) {
    if (result.recommended === "1"){
        document.getElementById("Disable_Recommended").checked = true;
        chrome.storage.local.set({recommended: "1"});
    }
    else{
        document.getElementById("Disable_Recommended").checked = false;
        chrome.storage.local.set({recommended: "0"});
    }
});

chrome.storage.local.get('disabled', function (result) {
    if(result.disabled) {
        if (result.disabled === "1"){
            document.getElementById("myonoffswitch").checked = true;
        }
        else{
            document.getElementById("myonoffswitch").checked = false;
        }
    }
    else{
        chrome.storage.local.set({disabled: "0"});
    }
});

chrome.storage.local.get('speed', function (result) {
    if(result.speed) {
        document.getElementById("Speed").value = result.speed
    }

});

update_textarea();

function set_playback_speed(){
    var x = document.getElementById("Speed").value;
    chrome.storage.local.set({speed: x});

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, "set_speed");
    });
}

function disable_recommendations(){
    if (document.getElementById("Disable_Recommended").checked){
        chrome.storage.local.set({recommended: "1"});
    }
    else{
        chrome.storage.local.set({recommended: "0"});
    }
}

function disable(){
    if (document.getElementById("myonoffswitch").checked){
        chrome.storage.local.set({disabled: "1"});
    }
    else{
        chrome.storage.local.set({disabled: "0"});
    }
}


function add(){
    var channelName = document.getElementById("AddChannel").value;
    if (channelName === ""){return;}

    chrome.storage.sync.get('whitelist', function (result) {
        if(result.whitelist) { 
            var wl = result.whitelist;
            for (let i = 0; i < wl.length; i++){
                if (wl[i] === channelName){return;}
            }
            wl.unshift(channelName);
            chrome.storage.sync.set({whitelist: wl});
            update_textarea();

        } else { // uninitialised
            chrome.storage.sync.set({whitelist: [channelName]});
            update_textarea();
        }
    });
    document.getElementById("AddChannel").value = "";
}

function remove_channel(){
    var channelName = document.getElementById("RemoveChannel").value;

    chrome.storage.sync.get('whitelist', function (result) {
        if(result.whitelist) { 
            var wl = result.whitelist;
            for (let i = 0; i < wl.length; i++){
                if (wl[i] === channelName){
                    wl.splice(i, 1);
                }
            }
            chrome.storage.sync.set({whitelist: wl});
            update_textarea();
        }
    });
    document.getElementById("RemoveChannel").value = "";
}

function remove_all(){
    chrome.storage.sync.clear();
    document.getElementById("List").value = "";
}

function update_textarea(){
    chrome.storage.sync.get('whitelist', function (result) {
        if(result.whitelist) { 
            var wl = result.whitelist;
            var out = "";
            for (let i = 0; i < wl.length; i++){
                out += wl[i] + '\n';
            }
            document.getElementById("List").value = out;
        }
    });
}
