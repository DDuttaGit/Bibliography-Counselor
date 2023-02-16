browser.browserAction.onClicked.addListener(async (tab) => {
  try {
    await browser.tabs.executeScript({
      file: "run.js"
    });
  } catch (err) {
    console.log(`failed to execute script: ${err}`);
  }
});
