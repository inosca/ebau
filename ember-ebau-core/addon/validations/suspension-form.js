import { validatePresence } from "ember-changeset-validations/validators";

export default {
  startDate: [validatePresence(true)],
  reason: [validatePresence(true)],
};
