import Controller from "@ember/controller";
import { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { assert } from "@ember/debug";
import { reads } from "@ember/object/computed";
import { computed, getWithDefault } from "@ember/object";
import QueryParams from "ember-parachute";

const queryParams = new QueryParams({
  displayedForm: {
    default: "",
    refresh: true
  }
});

export default Controller.extend(queryParams.Mixin, {
  calumaStore: service(),

  editController: controller("instances.edit"),
  instanceId: reads("editController.model"),
  instance: reads("editController.instance"),
  instanceTask: reads("editController.instanceTask"),

  embedded: computed(() => window !== window.top),

  reset() {
    this.resetQueryParams();
  },

  document: computed("model", "instance.documents.[]", function() {
    return this.getWithDefault("instance.documents", []).find(
      document => document.form.slug === this.model
    );
  }),

  disabled: computed(
    "document.form.{slug,meta.is-main-form}",
    "instance.meta.permissions",
    function() {
      const form = this.get("document.form.meta.is-main-form")
        ? "main"
        : this.get("document.form.slug");
      const permissions = this.getWithDefault("instance.meta.permissions", {});

      return !getWithDefault(permissions, form, []).includes("write");
    }
  ),

  pdfField: computed("model", "instance.documents.[]", function() {
    const slug = ["sb1", "sb2"].includes(this.model)
      ? "formulardownload-pdf-selbstdeklaration"
      : "formulardownload-pdf";

    const field = this.instance.findCalumaField(slug, this.model);

    assert(`Did not find field ${slug} in form ${this.model}`, field);

    return field;
  })
});
