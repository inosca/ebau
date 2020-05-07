import Component from "@ember/component";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";

export default Component.extend({
  router: service(),

  tagName: "li",

  classNameBindings: ["active:uk-active"],

  active: computed("module.link", "router.currentRouteName", function() {
    return new RegExp(`^${this.get("module.link")}.*$`).test(
      this.router.currentRouteName
    );
  })
});
