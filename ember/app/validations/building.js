import { validatePresence } from 'ember-changeset-validations/validators'

export default {
  adresse: validatePresence(true),
  'vers-nr': validatePresence(true),
  'kataster-nr': validatePresence(true),
  kategorie: validatePresence(true),
  heizungsart: validatePresence(true),
  'energietrager-heizung': validatePresence(true),
  'energietrager-warmwasser': validatePresence(true),
  leistung: validatePresence(false),
  geschosse: validatePresence(true),
  wohnraume: validatePresence(true),
  wohnungen: validatePresence(true)
}
