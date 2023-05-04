import Model, { belongsTo, hasMany } from "@ember-data/model";

export default class CirculationModel extends Model {
  @belongsTo("instance", { inverse: "circulations", async: true }) instance;
  @hasMany("activation", { inverse: "circulation", async: true }) activations;
}
