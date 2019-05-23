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
    return {
      ...(this.group ? { "X-CAMAC-GROUP": this.group } : {}),
      ...(this.role ? { "X-CAMAC-ROLE": this.role } : {})
    };
  })
});
