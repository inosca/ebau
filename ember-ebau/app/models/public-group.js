import Model, { attr, belongsTo } from "@ember-data/model";
import { get } from "@ember/object";

import config from "../config/environment";

export default class PublicGroup extends Model {
  @attr name;
  @belongsTo("public-role") role;
  @belongsTo("public-service") service;
}
