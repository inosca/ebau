import Controller from "@ember/controller";

import { computed } from "@ember/object";

export default Controller.extend({
  queryParams: ["section", "subSection", "group", "role"],
  section: null,
  subSection: null,
  group: null,
  role: null,

  isEmbedded: window !== window.top,

  headers: computed("group", "role", function() {
    const headers = {};
    if (this.get("group")) {
      headers["X-CAMAC-GROUP"] = this.get("group");
    }
    if (this.get("role")) {
      headers["X-CAMAC-GROUP"] = this.get("role");
    }
    return headers;
  })
});
