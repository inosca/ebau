import Component from "@ember/component";
import { computed } from "@ember/object";

export const ICON_PATH_BASE = "/assets/icons";

export default Component.extend({
  tagName: "span",

  classNames: ["pointer"],

  classNameBindings: ["directionClass"],

  click(e) {
    e.preventDefault();

    this["on-click"](`${this.direction > 0 ? "-" : ""}${this.key}`);
  },

  direction: computed("key", "sort", function() {
    let match = (this.sort || "").match(new RegExp(`^(-)?${this.key}$`));

    if (!match) {
      return 0;
    }

    return match.filter(Boolean).length > 1 ? -1 : 1;
  }),

  directionClass: computed("direction", function() {
    switch (this.direction) {
      case 1:
        return "sort-icon-asc";
      case -1:
        return "sort-icon-desc";
      case 0:
      default:
        return "sort-icon-neutral";
    }
  }),

  icon: computed("direction", function() {
    switch (this.direction) {
      case 1:
        return `${ICON_PATH_BASE}/sort-asc.svg`;
      case -1:
        return `${ICON_PATH_BASE}/sort-desc.svg`;
      case 0:
      default:
        return `${ICON_PATH_BASE}/sort-neutral.svg`;
    }
  })
});
