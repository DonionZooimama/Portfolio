
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request === "go"){
        go();
    }
    if (request === "set_speed"){
        set_speed();
    }
});

function go(){
    console.log("yeet1");
    var current_url = window.location.toString();

    if (current_url === "https://www.youtube.com/"){
        chrome.storage.local.get('recommended', function (result) {
            if (result.recommended){
                if (result.recommended === "1"){
                    remove_recommended();
                }
            }
        });
    }
    else{
        if (current_url.split("/")[3] === "channel" || current_url.split("/")[3] === "user"){return;}
        if (current_url.split("/")[3].split("?")[0] === "results"){return;}
        set_speed();

        chrome.storage.local.get('disabled', function (result) {
            if(result.disabled === "1") {
                window.setTimeout(check, 1500);
            }
        });
    } 
}

function set_speed(){
    chrome.storage.local.get('speed', function (result) {
        document.getElementsByTagName("video")[0].playbackRate = parseFloat(result.speed);
    });
}

function getElementByXpath(path) {
  return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function remove_recommended(){
    let data = document.getElementsByTagName("ytd-browse");
    data[0].parentNode.removeChild(data[0]);
}

function check(){
    var current_channel = getElementByXpath('//*[@id="owner-name"]/a').innerHTML;

    chrome.storage.local.set({channel: current_channel});
    console.log(current_channel);

    chrome.storage.sync.get('whitelist', function (result) {
        if(result.whitelist) { 
            var wl = result.whitelist;

            var is_lazy = true;
            for (var i = 0; i < wl.length; i++){
                if (current_channel === wl[i]){
                    is_lazy = false;
                }
            }
            if (is_lazy){
                chrome.runtime.sendMessage({redirect: "redirect.html"});
            }
        }
    });
}
