import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import getEbauNumberQuery from "camac-ng/gql/queries/get-ebau-number.graphql";

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

  @lastValue("fetchMeta") meta = null;
  @dropTask
  *fetchMeta() {
    return yield this.apollo.query(
      {
        query: getEbauNumberQuery,
        variables: { instanceId: parseInt(this.id) },
      },
      `allCases.edges.firstObject.node.meta`
    ) || null;
  }

  get ebauNumber() {
    return this.meta?.["ebau-number"];
  }

  get dossierNumber() {
    return this.meta?.["dossier-number"];
  }
}
