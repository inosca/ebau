import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";

import getCaseMetaQuery from "camac-ng/gql/queries/get-case-meta.graphql";

export default class InstanceModel extends Model {
  @queryManager apollo;

  @attr identifier;
  @attr name;
  @attr calumaForm;
  @attr meta;

  @belongsTo user;
  @belongsTo form;
  @belongsTo instanceState;
  @belongsTo location;

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
}
