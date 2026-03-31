import { service } from "@ember/service";
import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { trackedFunction } from "reactiveweb/function";

export default class ApplicantConfirmationRoundModel extends Model {
  @service session;
  @service fetch;
  @service store;

  @attr step;
  @attr status;
  @attr createdAt;
  @attr closedAt;

  @belongsTo("document", { async: true, inverse: null }) document;
  @belongsTo("instance", { async: true, inverse: null }) instance;
  @hasMany("applicant-confirmation", { async: true, inverse: "round" })
  confirmations;

  get isActive() {
    return ["running", "completed"].includes(this.status);
  }

  #currentUserConfirmation = trackedFunction(this, async () => {
    const confirmations = await this.confirmations;

    return (
      confirmations.find(
        (c) =>
          parseInt(c.belongsTo("user").id()) === parseInt(this.session.user.id),
      ) ?? null
    );
  });

  get currentUserConfirmation() {
    return this.#currentUserConfirmation.value;
  }

  async cancel() {
    const baseUrl = this.store
      .adapterFor(this.constructor.modelName)
      .buildURL(this.constructor.modelName, this.id);

    const response = await this.fetch.fetch(
      `${baseUrl}/cancel?include=confirmations`,
      { method: "POST" },
    );

    await this.store.pushPayload(await response.json());
  }

  async invalidate() {
    const baseUrl = this.store
      .adapterFor(this.constructor.modelName)
      .buildURL(this.constructor.modelName, this.id);

    const response = await this.fetch.fetch(
      `${baseUrl}/invalidate?include=confirmations`,
      { method: "POST" },
    );

    await this.store.pushPayload(await response.json());
  }
}
