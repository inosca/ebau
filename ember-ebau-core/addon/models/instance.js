import { inject as service } from "@ember/service";
import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { queryManager } from "ember-apollo-client";

export default class InstanceModel extends Model {
  @queryManager apollo;

  @service store;

  @attr identifier;
  @attr name;
  @attr calumaForm;
  @attr meta;
  @attr isModification;
  @attr isPaper;
  @attr dossierNumber;
  @attr ebauNumber;
  @attr decision;
  @attr decisionDate;
  @attr involvedAt;
  @attr isAfterDecision;
  @attr isInSB1;
  @attr rejectionFeedback;

  @belongsTo("user", { inverse: null, async: true, readOnly: true }) user;
  @belongsTo("form", { inverse: null, async: true, readOnly: true }) form;
  @belongsTo("instance-state", { inverse: null, async: true, readOnly: true })
  instanceState;
  @belongsTo("location", { inverse: null, async: true, readOnly: true })
  location;
  @belongsTo("instance-state", { inverse: null, async: true, readOnly: true })
  previousInstanceState;
  @belongsTo("public-service", { inverse: null, async: true, readOnly: true })
  activeService;

  @hasMany("service", { inverse: null, async: true, readOnly: true })
  circulationInitializerServices;
  @hasMany("circulation", { inverse: "instance", async: true, readOnly: true })
  circulations;
  @hasMany("service", { inverse: null, async: true, readOnly: true }) services;
  @hasMany("service", { inverse: null, async: false, readOnly: true })
  involvedServices;
  @hasMany("instance", { inverse: null, async: false, readOnly: true })
  linkedInstances;
  @hasMany("user", { inverse: null, async: true, readOnly: true })
  responsibleServiceUsers;
  @hasMany("keyword", { inverse: "instances", async: true }) keywords;

  unlink() {
    const adapter = this.store.adapterFor("instance");
    return adapter.unlink(this);
  }
}
