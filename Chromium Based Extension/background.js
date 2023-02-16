chrome.contextMenus.create({
    "id": "Bibliography Counselor",
    "title": "Fetch Bibs",
    "contexts": ["selection"]
}, () => chrome.runtime.lastError);

chrome.runtime.onInstalled.addListener((details) => {
    installReason(details)
});

chrome.action.onClicked.addListener((tab) => {
     chrome.scripting.executeScript({
        target: {tabId: tab.id},
        files: ["chooseEditor.js", "client.js", "user.js", "action.js", "run.js"],
        world: 'MAIN'
    });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    chrome.scripting.executeScript({
        target: {tabId: tab.id},
        files: ["chooseEditor.js", "client.js", "user.js", "action.js", "run.js"],
        world: 'MAIN'
    });
})

let installReason = (detail) => {
    if (detail.reason === "install") {
        chrome.tabs.create({
            url: "https://13.233.129.4/homepage.html"
        })}
    else if (detail.reason === "update") {
            console.log("Could not send notification in MV3");
        }
}
