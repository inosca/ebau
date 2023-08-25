import { getOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import saveDocumentMutation from "@projectcaluma/ember-form/gql/mutations/save-document.graphql";
import { parseDocument } from "@projectcaluma/ember-form/lib/parsers";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";

export default class GisApplyButtonComponent extends Component {
  @service intl;
  @service notification;
  @service fetch;
  @service calumaStore;

  @queryManager apollo;

  @tracked data = [];
  @tracked showModal = false;

  getData = dropTask(async () => {
    if (this.args.disabled) return;

    try {
      const params = Object.entries(this.args.params)
        .map(([key, value]) => `${key}=${value}`)
        .join("&");

      const response = await this.fetch.fetch(`/api/v1/gis/data?${params}`, {
        headers: { accept: "application/json" },
      });

      this.data = await response.json();
      this.showModal = true;
    } catch {
      this.notification.danger(this.intl.t("so-gis.apply-error"));
    }
  });

  applyData = dropTask(async () => {
    const success = await Promise.all(
      Object.entries(this.data).map(
        async ([question, value]) => await this.applyAnswer(question, value),
      ),
    );

    if (success.every(Boolean)) {
      this.showModal = false;
    }
  });

  async applyAnswer(question, { value, label, form = null }, document) {
    const doc = document ?? this.args.document;
    const field = doc.findField(question);

    try {
      if (field.questionType === "DynamicChoiceQuestion") {
        const option = field.options.find((o) => o.label === value);
        field.answer.value = option.slug;
      } else if (field.questionType === "TableQuestion") {
        field.answer.value = await this.applyTableAnswer(value, form);
      } else {
        field.answer.value = value;
      }

      await field.save.perform();
      return true;
    } catch {
      this.notification.danger(
        this.intl.t("so-gis.apply-answer-error", { label }),
      );
      return false;
    }
  }

  async applyTableAnswer(value, form) {
    const rawDocument = await this.apollo.mutate(
      {
        mutation: saveDocumentMutation,
        variables: { input: { form } },
      },
      "saveDocument.document",
    );

    const owner = getOwner(this);
    const Document = owner.factoryFor("caluma-model:document").class;

    const newDocument = this.calumaStore.push(
      new Document({
        raw: parseDocument(rawDocument),
        parentDocument: this.args.document,
        owner,
      }),
    );

    await Promise.all(
      Object.entries(value).map(
        async ([question, cell]) =>
          await this.applyAnswer(question, cell, newDocument),
      ),
    );

    return [newDocument];
  }
}
