// Loads Sine.
if (!Services.appinfo.inSafeMode) {
  try {
    const cmanifest = Services.dirsvc.get("UChrm", Ci.nsIFile);
    cmanifest.append("utils");
    cmanifest.append("chrome.manifest");
   
    if (cmanifest.exists()) {
      Components.manager.QueryInterface(Ci.nsIComponentRegistrar).autoRegister(cmanifest);
     
      const MODULE_LOADER = ChromeUtils.compileScript("chrome://userchromejs/content/module_loader.mjs");
      
      Services.obs.addObserver({
        observe(window) {
          window.addEventListener("DOMContentLoaded", async (event) => {
            const document = event.originalTarget;
            const window = document.defaultView;

            const path = window.location.pathname;
            if (path !== "/content/browser.xhtml" && 
                path !== "/content/messenger.xhtml" && 
                path !== "settings" && 
                path !== "preferences") return;
           
            document.allowUnsafeHTML = false;
           
            Object.defineProperty(window, "UC_API", {
              get: () => ChromeUtils.importESModule("chrome://userchromejs/content/uc_api.sys.mjs"),
              configurable: true,
              enumerable: true
            });
           
            MODULE_LOADER.then(m => m.executeInGlobal(window));
          }, { capture: true, once: false, passive: true });
        }
      }, "domwindowopened", false);
    }
  } catch (err) {}
}