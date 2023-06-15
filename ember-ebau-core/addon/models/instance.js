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

  @belongsTo user;
  @belongsTo form;
  @belongsTo instanceState;
  @belongsTo("instance-state") previousInstanceState;
  @belongsTo location;
  @belongsTo("public-service") activeService;

  @hasMany("service") circulationInitializerServices;
  @hasMany circulations;
  @hasMany services;
  @hasMany("service") involvedServices;
  @hasMany("instance", { inverse: null }) linkedInstances;

  unlink() {
    const adapter = this.store.adapterFor("instance");
    return adapter.unlink(this);
  }
}
