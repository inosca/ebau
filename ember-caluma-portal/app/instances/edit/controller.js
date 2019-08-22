import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { computed, getWithDefault } from "@ember/object";
import { reads } from "@ember/object/computed";
import { task } from "ember-concurrency";
import QueryParams from "ember-parachute";
import { ObjectQueryManager } from "ember-apollo-client";

const FEEDBACK_ATTACHMENT_SECTION = 3;

const queryParams = new QueryParams({
  group: {
    default: null,
    refresh: true
  }
});

export default Controller.extend(queryParams.Mixin, ObjectQueryManager, {
  fetch: service(),

  setup() {
    this.instanceTask.perform();
    this.feedbackTask.perform();
  },

  reset() {
    this.instanceTask.cancelAll({ resetState: true });
    this.feedbackTask.cancelAll({ resetState: true });

    this.resetQueryParams();
  },

  embedded: computed(() => window !== window.top),

  additionalForms: computed("instance.meta.permissions", function() {
    const permissions = this.getWithDefault("instance.meta.permissions", {});

    return ["nfd", "sb1", "sb2"].filter(form =>
      getWithDefault(permissions, form, []).includes("read")
    );
  }),

  instance: reads("instanceTask.lastSuccessful.value"),
  instanceTask: task(function*() {
    const instance = yield this.store.findRecord("instance", this.model, {
      include: "instance_state"
    });

    yield instance.getDocuments.perform();

    return instance;
  }).drop(),

  feedback: reads("feedbackTask.lastSuccessful.value"),
  feedbackTask: task(function*() {
    return yield this.store.query("attachment", {
      instance: this.model,
      attachment_sections: FEEDBACK_ATTACHMENT_SECTION,
      include: "attachment_sections"
    });
  }).drop()
});
