import Model, { attr } from "@ember-data/model";

export default class PublicCalumaInstanceModel extends Model {
  @attr documentId;
  @attr instanceId;
  @attr dossierNr;
  @attr municipality;
  @attr applicant;
  @attr intent;
  @attr street;
  @attr parcels;
  @attr publicationEndDate;
}
