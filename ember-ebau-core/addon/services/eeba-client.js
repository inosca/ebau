import Service, { service } from "@ember/service";

import { EEBA_ANSWER_QUESTIONS, EEBA_STATE } from "ember-ebau-core/config/eeba";

export default class EebaClientService extends Service {
  @service fetch;

  // performing the eEBA refresh will run in a debounced timeout to prevent
  // conflicting multiple saves/refreshes during quick consequent save actions.
  // This can occur e.g. when using a auto-fill extension in the browser.
  debounce = {
    timeout: null,
    fields: {},
  };

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

  async onSaveEebaRefresh(document, question) {
    clearTimeout(this.debounce.timeout);

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
      // If there are still fields in the debounce list, we keep the timeout
      // to perform the refresh for those.
      return (this.debounce.timeout = setTimeout(
        () => this.performEebaRefresh(),
        250,
      ));
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
        this.debounce.fields[slug] = await document
          .findField(slug)
          ?.refreshAnswer.linked();
      });

    return (this.debounce.timeout = setTimeout(
      () => this.performEebaRefresh(),
      250,
    ));
  }

  /**
   * Performs the actual debounced refresh for all queued fields.
   */
  async performEebaRefresh() {
    const fields = this.debounce.fields;
    this.debounce.timeout = null;
    this.debounce.fields = {};

    return await Promise.all(
      Object.values(fields).map(async (refresh) => {
        try {
          return await refresh?.perform();
        } catch {
          return Promise.resolve();
        }
      }),
    );
  }

  mapQuery(params) {
    const query = Object.entries(params)
      .map(([k, v]) => `${k}=${v}`)
      .join("&");

    return query ? `?${query}` : "";
  }
}
