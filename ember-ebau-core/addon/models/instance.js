import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { inject as service } from "@ember/service";
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

  @belongsTo user;
  @belongsTo form;
  @belongsTo instanceState;
  @belongsTo location;

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
