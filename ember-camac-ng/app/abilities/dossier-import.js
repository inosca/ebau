import { Ability } from "ember-can";

export default class extends Ability {
  get canStart() {
    return this.model?.status === "verified";
  }

  get canDelete() {
    return ["verified", "failed"].includes(this.model?.status);
  }
}
