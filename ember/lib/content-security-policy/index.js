"use strict";

module.exports = {
  name: require("./package").name,

  isDevelopingAddon() {
    return true;
  },

  contentFor(type, config) {
    if (type === "head") {
      return `<meta http-equiv="Content-Security-Policy" content="frame-ancestors ${config.APP.internalHost}">`;
    }

    return "";
  },
};
