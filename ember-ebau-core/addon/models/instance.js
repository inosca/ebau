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

  @belongsTo("user", { inverse: null, async: true }) user;
  @belongsTo("form", { inverse: null, async: true }) form;
  @belongsTo("instance-state", { inverse: null, async: true }) instanceState;
  @belongsTo("location", { inverse: null, async: true }) location;
  @belongsTo("instance-state", { inverse: null, async: true })
  previousInstanceState;
  @belongsTo("public-service", { inverse: null, async: true }) activeService;

  @hasMany("service", { inverse: null, async: true })
  circulationInitializerServices;
  @hasMany("circulation", { inverse: "instance", async: true }) circulations;
  @hasMany("service", { inverse: null, async: true }) services;
  @hasMany("service", { inverse: null, async: false }) involvedServices;
  @hasMany("instance", { inverse: null, async: true }) linkedInstances;

  unlink() {
    const adapter = this.store.adapterFor("instance");
    return adapter.unlink(this);
  }
}
