import { validatePresence } from "ember-changeset-validations/validators";

export default {
  addressedService: [validatePresence(true)],
  title: [validatePresence(true)],
  deadline: [validatePresence(true)],
};
