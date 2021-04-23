import Model, { attr } from "@ember-data/model";

export default class PublicCalumaInstanceModel extends Model {
  @attr instanceId;
  @attr dossierNr;
  @attr municipality;
  @attr applicant;
  @attr street;
  @attr parcels;
}
