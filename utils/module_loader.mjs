{
  import("chrome://userscripts/content/sine.uc.mjs")
  .catch(err => {
    console.error(new Error(`@ sine.uc.mjs:${err.lineNumber}`, { cause: err }));
  });
}