import DOMPurify from "dompurify";
import showdown from "showdown";

export function initialize() {
  showdown.extension("DOMPurify", function () {
    return [
      {
        type: "output",
        filter(dirty) {
          return DOMPurify.sanitize(dirty, { USE_PROFILES: { html: true } });
        },
      },
    ];
  });
}

export default {
  name: "register-showdown-extensions",
  initialize,
};
