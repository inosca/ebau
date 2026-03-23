import { validatePresence } from "ember-changeset-validations/validators";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default {
  startDate: [validatePresence(true)],
  reason: [validatePresence(hasFeature("deadlines.manualSuspensionReason"))],
};
