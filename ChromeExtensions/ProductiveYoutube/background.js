console.log("yeet 2.0");

chrome.tabs.onUpdated.addListener( function (tabId, changeInfo, tab) {
    chrome.tabs.sendMessage(tab.id, "go");
});

chrome.runtime.onMessage.addListener(function(request, sender) {
    chrome.tabs.update(sender.tab.id, {url: request.redirect});
});
