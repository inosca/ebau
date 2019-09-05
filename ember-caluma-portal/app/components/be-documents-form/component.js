import Component from "@ember/component";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";
import { computed } from "@ember/object";
import { reads, filterBy } from "@ember/object/computed";
import { A } from "@ember/array";
import { all } from "rsvp";
import { ComponentQueryManager } from "ember-apollo-client";
import { assert } from "@ember/debug";

const DEFAULT_CATEGORY = "weitere-unterlagen";
const ALLOWED_MIMETYPES = ["image/png", "image/jpeg", "application/pdf"];

export default Component.extend(ComponentQueryManager, {
  intl: service(),
  fetch: service(),
  notification: service(),
  store: service(),

  didReceiveAttrs() {
    this._super(...arguments);

    this.data.perform();
  },

  section: reads("fieldset.field.question.meta.attachment-section"),
  deletable: computed(
    "disabled",
    "context.instance.instanceState.name",
    function() {
      const state = this.get("context.instance.instanceState.name");

      // in certain states the form will be editable but deleting is disallowed
      return (
        !this.disabled &&
        state &&
        !["Zurückgewiesen", "In Korrektur"].includes(state)
      );
    }
  ),

  data: task(function*() {
    assert(
      "An attachment section must be passed to the question's meta",
      this.section
    );

    return yield this.store.query("attachment", {
      instance: this.context.instanceId,
      attachment_sections: this.section
    });
  }),

  allVisibleTags: computed(
    "fieldset.fields.@each.{hidden,isNew,questionType}",
    function() {
      return this.fieldset.fields.filter(
        f => !f.hidden && f.isNew && f.questionType === "MultipleChoiceQuestion"
      );
    }
  ),

  allRequiredTags: filterBy("allVisibleTags", "optional", false),
  allOptionalTags: filterBy("allVisibleTags", "optional", true),

  requiredTags: computed("allRequiredTags.[]", function() {
    return this.allRequiredTags.reduce((tree, tag) => {
      const category = tag.question.meta.documentCategory || DEFAULT_CATEGORY;

      return Object.assign(tree, {
        [category]: [...(tree[category] || []), tag]
      });
    }, {});
  }),

  optionalTags: computed("allOptionalTags.[]", "intl.locale", function() {
    return this.allOptionalTags.reduce((grouped, tag) => {
      const category = this.intl.t(
        `documents.tags.${tag.question.meta.documentCategory ||
          DEFAULT_CATEGORY}`
      );

      let group = grouped.find(g => g.groupName === category);

      if (!group) {
        group = {
          groupName: category,
          options: []
        };

        grouped.push(group);
      }

      group.options.push(tag);

      return grouped;
    }, []);
  }),

  selectedRequiredTags: A([]),
  selectedOptionalTags: A([]),
  allSelectedTags: computed(
    "selectedRequiredTags.[]",
    "selectedOptionalTags.[]",
    function() {
      return [
        ...new Set([...this.selectedRequiredTags, ...this.selectedOptionalTags])
      ];
    }
  ),

  selectFile: task(function*(file) {
    this.set("file", file);

    if (!this.allVisibleTags.length) {
      yield this.save.perform();
    }
  }),

  saveFile: task(function*() {
    if (!ALLOWED_MIMETYPES.includes(this.file.blob.type)) {
      this.notification.danger(this.intl.t("documents.wrongMimeType"));

      throw new Error();
    }

    const formData = new FormData();

    formData.append("instance", this.context.instanceId);
    formData.append("attachment_sections", this.section);
    formData.append(
      "context",
      JSON.stringify({
        tags: this.allSelectedTags.map(
          ({ question: { slug, label } }) => slug || label
        )
      })
    );
    formData.append("path", this.file.blob, this.file.name);

    const response = yield this.fetch.fetch("/api/v1/attachments", {
      method: "post",
      body: formData,
      headers: {
        "content-type": undefined
      }
    });

    if (!response.ok) {
      const {
        errors: [{ detail: e }]
      } = yield response.json();

      throw new Error(e);
    }
  }),

  saveFields: task(function*(clear = false) {
    const fields = this.allSelectedTags.filter(
      t => t.question.slug && t.question.__typename === "MultipleChoiceQuestion"
    );

    yield all(
      fields.map(async field => {
        field.set(
          "answer.value",
          clear
            ? []
            : [
                field.get(
                  "question.multipleChoiceOptions.edges.firstObject.node.slug"
                )
              ]
        );

        await field.save.perform();
        await field.validate.perform();
      })
    );
  }),

  save: task(function*() {
    try {
      yield this.saveFile.perform();
      yield this.saveFields.perform();

      this._reset();

      yield this.data.perform();

      this.notification.success(this.intl.t("documents.uploadSuccess"));
    } catch (e) {
      /* eslint-disable-next-line no-console */
      console.error(e);
      this.notification.danger(this.intl.t("documents.uploadError"));

      yield this.saveFields.perform(true);
    }
  }),

  delete: task(function*(confirmed = false, attachment) {
    try {
      if (!this.deletable) return;

      if (!confirmed) {
        this.set("attachmentToDelete", attachment);

        return;
      }

      yield all(
        attachment.tags
          .map(({ slug }) => this.fieldset.document.findField(slug))
          .map(async field => {
            field.set("answer.value", null);

            await field.save.perform();

            // something with the isNew property of the field isn't quite right
            // yet so we need to trigger it's update manually for now
            // See https://github.com/projectcaluma/ember-caluma/issues/459
            field.notifyPropertyChange("isNew");
          })
      );

      yield attachment.destroyRecord();
      yield this.data.perform();

      this.notification.success(this.intl.t("documents.deleteSuccess"));

      this.set("attachmentToDelete", null);
    } catch (e) {
      /* eslint-disable-next-line no-console */
      console.error(e);
      this.notification.danger(this.intl.t("documents.deleteError"));
    }
  }),

  _reset() {
    this.setProperties({
      file: null,
      selectedOptionalTags: A([]),
      selectedRequiredTags: A([])
    });
  },

  actions: {
    reset() {
      this._reset();
    },

    updateSelectedRequiredTags(tag) {
      const selectedRequiredTags = new Set(this.selectedRequiredTags);

      selectedRequiredTags.delete(tag) || selectedRequiredTags.add(tag);

      this.set("selectedRequiredTags", [...selectedRequiredTags]);
    }
  }
});
