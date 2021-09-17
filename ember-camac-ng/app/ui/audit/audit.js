import { inject as service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

export default class Audit {
  @service store;
  @service shoebox;

  constructor(raw, caseData) {
    this._raw = raw;
    this._caseData = caseData;
  }

  get instanceId() {
    return this._caseData.instanceId;
  }

  get id() {
    return decodeId(this._raw.id);
  }

  get type() {
    return this._raw.form.name;
  }

  get municipality() {
    return this.store.peekRecord("service", this._raw.createdByGroup);
  }

  get modifiedByUser() {
    return (
      this._raw.modifiedContentByUser &&
      this.store
        .peekAll("public-user")
        .find((user) => user.username === this._raw.modifiedContentByUser)
    );
  }

  get modifiedByService() {
    return (
      this._raw.modifiedContentByGroup &&
      this.store.peekRecord("service", this._raw.modifiedContentByGroup)
    );
  }

  get modifiedAt() {
    return this._raw.modifiedContentAt;
  }

  get form() {
    return this._raw.form.slug;
  }
}
