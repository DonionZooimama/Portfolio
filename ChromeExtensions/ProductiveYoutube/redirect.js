
update_textarea();

chrome.storage.local.get('channel', function (result) {
    if(result.channel){ 
        document.getElementById("AddChannel").value = result.channel;
    }
});

document.getElementById("AddChannel").addEventListener("change", add);
document.getElementById("RemoveChannel").addEventListener("change", remove_channel);
document.getElementById("Add").addEventListener("click", add);
document.getElementById("Remove").addEventListener("click", remove_channel);
document.getElementById("RemoveAll").addEventListener("click", remove_all);

document.getElementById("Pay").addEventListener("click", function(){chrome.tabs.create({"url": "donate.html"});});

function add(){
    var channelName = document.getElementById("AddChannel").value;
    if (channelName === ""){return;}

    chrome.storage.sync.get('whitelist', function (result) {
        if(result.whitelist) { 
            var wl = result.whitelist;
            for (let i = 0; i < wl.length; i++){
                if (wl[i] === channelName){return;}
            }
            wl.push(channelName);
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
