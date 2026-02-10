import Service, { service } from "@ember/service";
import { task, timeout } from "ember-concurrency";

import { EEBA_ANSWER_QUESTIONS, EEBA_STATE } from "ember-ebau-core/config/eeba";

export default class EebaClientService extends Service {
  @service fetch;

  // performing the eEBA refresh will run in a debounced timeout to prevent
  // conflicting multiple saves/refreshes during quick consequent save actions.
  // This can occur e.g. when using a auto-fill extension in the browser.
  debounceFields = {};

  async checkIntegration(instanceId, params = {}, headers = {}) {
    const fullQuery = this.mapQuery(params);
    const response = await this.fetch.fetch(
      `/api/v1/instances/${instanceId}/check-eeba-integration${fullQuery}`,
      {
        method: "POST",
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
          ...headers,
        },
      },
    );

    return response?.json();
  }

  onSaveEebaRefresh = task(
    { restartable: true },
    async (document, question) => {
      const eebaStateField = document.findField(EEBA_ANSWER_QUESTIONS.STATE);
      const linkedFields =
        eebaStateField?.question?.raw?.meta?.eebaLinkedFields || [];

      // Stop if the eEBA state field is not present, or if there are no linked fields,
      // matching the question slug.
      if (
        !eebaStateField ||
        linkedFields.length === 0 ||
        !linkedFields.includes(question.slug)
      ) {
        return await this.performEebaRefresh.perform(document);
      }

      const isDirtyField = document.findField(EEBA_ANSWER_QUESTIONS.IS_DIRTY);
      const stateField = document.findField(EEBA_ANSWER_QUESTIONS.STATE);
      const isDirtyYes = `${EEBA_ANSWER_QUESTIONS.IS_DIRTY}-ja`;

      // mark the eEBA as dirty if the question is not already set to dirty.
      if (
        question.slug !== EEBA_ANSWER_QUESTIONS.IS_DIRTY &&
        isDirtyField &&
        isDirtyField.answer.value !== isDirtyYes
      ) {
        isDirtyField.answer.value = isDirtyYes;
        await isDirtyField.save.perform();

        // if the eEBA was already completed before, but a change was made,
        // the result is invalidated so we reset the eEBA state answer to NONE.
        if (stateField.answer.value === EEBA_STATE.COMPLETED) {
          stateField.answer.value = EEBA_STATE.NONE;
          await stateField.save.perform();
        }
      }

      // refresh all linked fields except the one that was just saved.
      // add all these fields to the debounce list for refreshing.
      Object.values(EEBA_ANSWER_QUESTIONS)
        .filter((slug) => slug !== question.slug)
        .forEach(async (slug) => {
          this.debounceFields[slug] = true;
        });

      return await this.performEebaRefresh.perform(document);
    },
  );

  /**
   * Performs the actual debounced refresh for all queued fields.
   */
  performEebaRefresh = task({ restartable: true }, async (document) => {
    try {
      await timeout(250);
      const fieldSlugs = Object.keys(this.debounceFields);
      this.debounceFields = {};
      await Promise.all(
        fieldSlugs.map((slug) =>
          document.findField(slug)?.refreshAnswer.linked().perform(),
        ),
      );
    } catch (e) {
      console.error("Error during eEBA refresh task:", e);

      throw e;
    }
  });

  mapQuery(params) {
    const query = Object.entries(params)
      .map(([k, v]) => `${k}=${v}`)
      .join("&");

    return query ? `?${query}` : "";
  }
}
