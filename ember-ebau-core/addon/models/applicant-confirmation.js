import { service } from "@ember/service";
import Model, { attr, belongsTo } from "@ember-data/model";

export default class ApplicantConfirmationModel extends Model {
  @service fetch;
  @service store;

  @attr status;
  @attr roles;
  @attr displayName;
  @attr("date") createdAt;
  @attr("date") closedAt;

  @belongsTo("user", { async: true, inverse: null }) user;
  @belongsTo("applicant-confirmation-round", {
    async: true,
    inverse: "confirmations",
  })
  round;

  async confirm() {
    const baseUrl = this.store
      .adapterFor(this.constructor.modelName)
      .buildURL(this.constructor.modelName, this.id);

    const response = await this.fetch.fetch(
      `${baseUrl}/confirm?include=round`,
      { method: "POST" },
    );

    await this.store.pushPayload(await response.json());
  }
}
