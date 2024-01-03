import { getOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import saveDocumentMutation from "@projectcaluma/ember-form/gql/mutations/save-document.graphql";
import { parseDocument } from "@projectcaluma/ember-form/lib/parsers";
import { queryManager } from "ember-apollo-client";
import { dropTask, task, timeout } from "ember-concurrency";

function countAnswers(data) {
  const rootCount = Object.keys(data).length;

  const childrenCount = Object.values(data)
    .filter(({ value, form = null }) => form && Array.isArray(value))
    .flatMap(({ value }) => value.map((row) => countAnswers(row)))
    .reduce((a, b) => a + b, 0);

  return rootCount + childrenCount;
}

export default class GisApplyButtonComponent extends Component {
  @service intl;
  @service notification;
  @service fetch;
  @service calumaStore;

  @queryManager apollo;

  @tracked data = [];
  @tracked showModal = false;

  @tracked totalAnswers = 0;
  @tracked appliedAnswers = 0;

  getData = dropTask(async () => {
    if (this.args.disabled) return;

    try {
      const params = Object.entries(this.args.params)
        .map(([key, value]) => `${key}=${value}`)
        .join("&");

      this.args.onGetData?.();

      const response = await this.fetch.fetch(`/api/v1/gis/data?${params}`, {
        headers: { accept: "application/json" },
      });

      const { task_id, errors = [] } = await response.json();

      if (errors.length) {
        errors.forEach(({ detail }) => {
          this.notification.danger(detail);
        });
      }

      const { data } = await this.pollData.perform(task_id);

      this.data = data;
      this.showModal = true;
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("so-gis.apply-error"));
    }
  });

  pollData = task(async (taskId) => {
    this.notification.warning(this.intl.t("gis.loadingHint"));

    let response;

    while (!response || response.status === 202) {
      /* eslint-disable no-await-in-loop */
      response = await this.fetch.fetch(`/api/v1/gis/data/${taskId}`, {
        headers: { accept: "application/json" },
      });

      if (!response.ok) {
        throw new Error("Error while polling GIS task results.");
      }

      await timeout(1000);
      /* eslint-enable no-await-in-loop */
    }

    return await response.json();
  });

  applyData = dropTask(async () => {
    this.totalAnswers = countAnswers(this.data);

    const success = await Promise.all(
      Object.entries(this.data).map(
        async ([question, value]) => await this.applyAnswer(question, value),
      ),
    );

    if (success.every(Boolean)) {
      this.showModal = false;
    }

    this.totalAnswers = 0;
    this.appliedAnswers = 0;
  });

  async applyAnswer(question, { value, label, form = null }, document) {
    const doc = document ?? this.args.document;
    const field = doc.findField(question);

    try {
      if (field.questionType === "DynamicChoiceQuestion") {
        const option = field.options.find((o) => o.label === value);
        field.answer.value = option.slug;
      } else if (field.questionType === "MultipleChoiceQuestion") {
        field.answer.value = value.map((r) => r.value);
      } else if (field.questionType === "TableQuestion") {
        field.answer.value = await this.applyTableAnswer(value, form);
      } else {
        field.answer.value = value;
      }

      await field.validate.perform();
      await field.save.perform();
      return true;
    } catch {
      this.notification.danger(
        this.intl.t("so-gis.apply-answer-error", { label }),
      );
      return false;
    } finally {
      this.appliedAnswers += 1;
    }
  }

  async applyTableAnswer(value, form) {
    return Promise.all(
      value.map(async (row) => {
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
          Object.entries(row).map(
            async ([question, cell]) =>
              await this.applyAnswer(question, cell, newDocument),
          ),
        );

        return newDocument;
      }),
    );
  }
}
