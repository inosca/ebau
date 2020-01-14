import { A } from "@ember/array";
import Component from "@ember/component";
import { assert } from "@ember/debug";
import { computed, getWithDefault } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import config from "ember-caluma-portal/config/environment";
import { task } from "ember-concurrency";
import { all } from "rsvp";

const DEFAULT_CATEGORY = "weitere-unterlagen";

export default Component.extend({
  intl: service(),
  fetch: service(),
  notification: service(),
  store: service(),

  apollo: queryManager(),

  /* eslint-disable-next-line ember/no-attrs-snapshot */
  didReceiveAttrs(...args) {
    this._super(...args);

    this.data.perform();
  },

  init(...args) {
    this._super(...args);

    this.set("allowedMimetypes", config.ebau.attachments.allowedMimetypes);
  },

  rootFormSlug: reads("fieldset.document.rootForm.slug"),
  showHint: computed("rootFormSlug", function() {
    return this.get("rootFormSlug").includes("baugesuch");
  }),

  section: reads("fieldset.field.question.meta.attachment-section"),
  deletable: computed(
    "disabled",
    "context.instance.instanceState.id",
    function() {
      const state = this.get("context.instance.instanceState.id");

      // In certain states the form will be editable but deleting is disallowed.
      //   State IDs according to /admin/resource_instance-state
      //   10000: Zurückgewiesen
      //   20007: In Korrektur

      return !this.disabled && !["10000", "20007"].includes(state);
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
    "fieldset.fields.@each.{hidden,value,questionType}",
    function() {
      return this.fieldset.fields.filter(
        field =>
          !field.hidden && field.questionType === "MultipleChoiceQuestion"
      );
    }
  ),

  savedTags: computed("data.lastSuccessful.value.content", function() {
    return [
      ...new Set(
        this.getWithDefault("data.lastSuccessful.value", [])
          .map(attachment => getWithDefault(attachment, "context.tags", []))
          .reduce((tags, tag) => tags.concat(tag), [])
      )
    ];
  }),

  allRequiredTags: computed("allVisibleTags.[]", "savedTags.[]", function() {
    return this.allVisibleTags.filter(
      tag => !tag.optional && !this.savedTags.includes(tag.question.slug)
    );
  }),

  allOptionalTags: computed("allVisibleTags.[]", "savedTags.[]", function() {
    return this.allVisibleTags.filter(
      tag => tag.optional || this.savedTags.includes(tag.question.slug)
    );
  }),

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
    if (
      !config.ebau.attachments.allowedMimetypes.includes(this.file.blob.type)
    ) {
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
        errors: [{ detail: error }]
      } = yield response.json();

      throw new Error(error);
    }
  }),

  saveFields: task(function*(clear = false) {
    const fields = this.allSelectedTags.filter(
      tag =>
        tag.question.slug &&
        tag.question.__typename === "MultipleChoiceQuestion"
    );

    yield all(
      fields
        .filter(field => field.isNew)
        .map(async field => {
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
    } catch (error) {
      /* eslint-disable-next-line no-console */
      console.error(error);
      this.notification.danger(this.intl.t("documents.uploadError"));

      yield this.saveFields.perform(true);
    }
  }),

  delete: task(function*(confirmed = false, attachment) {
    try {
      if (!this.deletable) {
        return;
      }

      if (!confirmed) {
        this.set("attachmentToDelete", attachment);

        return;
      }

      yield attachment.destroyRecord();
      yield this.data.perform();

      yield all(
        attachment.tags
          .map(({ slug }) => this.fieldset.document.findField(slug))
          .filter(field => !this.savedTags.includes(field.question.slug))
          .map(async field => {
            field.set("answer.value", []);

            await field.save.perform();
          })
      );

      this.notification.success(this.intl.t("documents.deleteSuccess"));

      this.set("attachmentToDelete", null);
    } catch (error) {
      /* eslint-disable-next-line no-console */
      console.error(error);
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
