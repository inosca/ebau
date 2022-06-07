import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";

import getCaseMetaQuery from "ember-ebau-core/gql/queries/get-case-meta.graphql";

export default class InstanceModel extends Model {
  @queryManager apollo;

  @service store;

  @attr identifier;
  @attr name;
  @attr calumaForm;
  @attr meta;
  @attr isModification;

  @belongsTo user;
  @belongsTo form;
  @belongsTo instanceState;
  @belongsTo location;

  @hasMany("service") circulationInitializerServices;
  @hasMany circulations;
  @hasMany services;
  @hasMany("service") involvedServices;
  @hasMany("instance") linkedInstances;

  @lastValue("fetchCaseMeta") _caseMeta = null;
  @dropTask
  *fetchCaseMeta() {
    return yield this.apollo.query(
      {
        query: getCaseMetaQuery,
        variables: { instanceId: parseInt(this.id) },
      },
      `allCases.edges.firstObject.node.meta`
    ) || null;
  }

  get ebauNumber() {
    return this._caseMeta?.["ebau-number"];
  }

  get dossierNumber() {
    return this._caseMeta?.["dossier-number"];
  }

  unlink() {
    const adapter = this.store.adapterFor("instance");
    return adapter.unlink(this);
  }
}
