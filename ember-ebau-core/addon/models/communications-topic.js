import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class CommunicationTopicModel extends Model {
  @attr subject;
  @attr hasUnread;
  @attr dossierNumber;
  @attr("date") created;
  @attr("date") lastMessageDate;
  @attr({ defaultValue: true }) allowReplies;
  @attr initiatedByEntity;
  @attr involvedEntities;

  @belongsTo("instance", { inverse: null, async: true }) instance;
  @belongsTo("user", { inverse: null, async: true }) initiatedBy;
  @hasMany("user", { inverse: null, async: true }) responsibleServiceUsers;
  @hasMany("instance-mark", { inverse: null, async: true, readOnly: true })
  instanceMarks;

  get instanceIdentifier() {
    if (hasFeature("communications.hideInstanceId")) {
      return this.dossierNumber;
    }

    const instanceId = this.belongsTo("instance").id();

    if (this.dossierNumber) {
      return `${this.dossierNumber} (${instanceId})`;
    }

    return instanceId;
  }
}
