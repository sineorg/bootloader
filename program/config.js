// Loads Sine.
if (!Services.appinfo.inSafeMode) {
  try {
    const cmanifest = Services.dirsvc.get("UChrm", Ci.nsIFile);
    cmanifest.append("utils");
    cmanifest.append("chrome.manifest");
   
    if (cmanifest.exists()) {
      Components.manager.QueryInterface(Ci.nsIComponentRegistrar).autoRegister(cmanifest);
      ChromeUtils.importESModule("chrome://userscripts/content/sine.sys.mjs");
    }
  } catch (err) {}
}
