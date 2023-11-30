import { validatePresence } from "ember-changeset-validations/validators";

export default {
  service: [validatePresence(true)],
  accessLevel: [validatePresence(true)],
};
