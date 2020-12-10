import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import getEbauNumberQuery from "camac-ng/gql/queries/get-ebau-number";

export default class InstanceModel extends Model {
  @queryManager apollo;

  @attr identifier;
  @attr name;
  @attr calumaForm;

  @belongsTo user;
  @belongsTo form;
  @belongsTo instanceState;

  @hasMany circulations;
  @hasMany services;
  @hasMany("service") involvedServices;

  @lastValue("fetchEbauNumber") ebauNumber = null;
  @dropTask
  *fetchEbauNumber() {
    return yield this.apollo.query(
      {
        query: getEbauNumberQuery,
        variables: { instanceId: parseInt(this.id) },
      },
      "allCases.edges.firstObject.node.meta.ebau-number"
    ) || null;
  }
}
