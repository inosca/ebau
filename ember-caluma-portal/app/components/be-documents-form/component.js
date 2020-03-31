import { A } from "@ember/array";
import Component from "@ember/component";
import { assert } from "@ember/debug";
import { computed, getWithDefault, action } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import config from "ember-caluma-portal/config/environment";
import { dropTask } from "ember-concurrency-decorators";
import { all } from "rsvp";

const DEFAULT_CATEGORY = "weitere-unterlagen";

export default class BeDocumentsFormComponent extends Component {
  @service intl;
  @service fetch;
  @service notification;
  @service store;

  @queryManager apollo;

  constructor(...args) {
    super(...args);

    this.set("allowedMimetypes", config.ebau.attachments.allowedMimetypes);
  }

  @reads("fieldset.document.rootForm.slug") rootFormSlug;
  @computed("rootFormSlug")
  get showHint() {
    return this.rootFormSlug.includes("baugesuch");
  }

  @computed(
    "document.{jexl,jexlContext}",
    "fieldset.field.question.meta.attachment-section"
  )
  get section() {
    return this.document.jexl.evalSync(
      this.get("fieldset.field.question.meta.attachment-section"),
      this.document.jexlContext
    );
  }

  @computed("disabled", "context.instance.instanceState.id")
  get deletable() {
    const state = this.get("context.instance.instanceState.id");

    // In certain states the form will be editable but deleting is disallowed.
    //   State IDs according to /admin/resource_instance-state
    //   10000: Zurückgewiesen
    //   20007: In Korrektur

    return !this.disabled && !["10000", "20007"].includes(state);
  }

  @dropTask
  *data() {
    assert(
      "An attachment section must be passed to the question's meta",
      this.section
    );

    return yield this.store.query("attachment", {
      instance: this.context.instanceId,
      attachment_sections: this.section
    });
  }

  @computed("fieldset.fields.@each.{hidden,value,questionType}")
  get allVisibleTags() {
    return this.fieldset.fields.filter(
      field => !field.hidden && field.questionType === "MultipleChoiceQuestion"
    );
  }

  @computed("data.lastSuccessful.value.content")
  get savedTags() {
    return [
      ...new Set(
        this.getWithDefault("data.lastSuccessful.value", [])
          .map(attachment => getWithDefault(attachment, "context.tags", []))
          .reduce((tags, tag) => tags.concat(tag), [])
      )
    ];
  }

  @computed("allVisibleTags.[]", "savedTags.[]")
  get allRequiredTags() {
    return this.allVisibleTags.filter(
      tag => !tag.optional && !this.savedTags.includes(tag.question.slug)
    );
  }

  @computed("allVisibleTags.[]", "savedTags.[]")
  get allOptionalTags() {
    return this.allVisibleTags.filter(
      tag => tag.optional || this.savedTags.includes(tag.question.slug)
    );
  }

  @computed("allRequiredTags.[]")
  get requiredTags() {
    return this.allRequiredTags.reduce((tree, tag) => {
      const category = tag.question.meta.documentCategory || DEFAULT_CATEGORY;

      return Object.assign(tree, {
        [category]: [...(tree[category] || []), tag]
      });
    }, {});
  }

  @computed("allOptionalTags.[]", "intl.locale")
  get optionalTags() {
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
  }

  selectedRequiredTags = A([]);
  selectedOptionalTags = A([]);
  @computed("selectedRequiredTags.[]", "selectedOptionalTags.[]")
  get allSelectedTags() {
    return [
      ...new Set([...this.selectedRequiredTags, ...this.selectedOptionalTags])
    ];
  }

  @dropTask
  *selectFile(file) {
    this.set("file", file);

    if (!this.allVisibleTags.length) {
      yield this.save.perform();
    }
  }

  @dropTask
  *saveFile() {
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
  }

  @dropTask
  *saveFields(clear = false) {
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
  }

  @dropTask
  *save() {
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
  }

  @dropTask
  *delete(confirmed = false, attachment) {
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
  }

  _reset() {
    this.setProperties({
      file: null,
      selectedOptionalTags: A([]),
      selectedRequiredTags: A([])
    });
  }

  @action
  reset() {
    this._reset();
  }

  @action
  updateSelectedRequiredTags(tag) {
    const selectedRequiredTags = new Set(this.selectedRequiredTags);

    selectedRequiredTags.delete(tag) || selectedRequiredTags.add(tag);

    this.set("selectedRequiredTags", [...selectedRequiredTags]);
  }
}
