import Service, { service } from "@ember/service";

import { EEBA_ANSWER_QUESTIONS, EEBA_STATE } from "ember-ebau-core/config/eeba";

export default class EebaClientService extends Service {
  @service fetch;

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
      return;
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
    return await Promise.all(
      Object.values(EEBA_ANSWER_QUESTIONS)
        .filter((slug) => slug !== question.slug)
        .map((slug) => {
          try {
            return document.findField(slug)?.refreshAnswer.linked().perform();
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
