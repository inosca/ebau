import Model, { belongsTo, hasMany } from "@ember-data/model";

export default class CirculationModel extends Model {
  @belongsTo instance;
  @hasMany activations;
}
