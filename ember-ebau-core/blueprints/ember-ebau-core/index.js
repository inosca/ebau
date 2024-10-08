"use strict";

module.exports = {
  normalizeEntityName() {}, // no-op since we're just adding dependencies

  afterInstall() {
    return this.addAddonsToProject({
      packages: [
        { name: "@projectcaluma/ember-form" },
        { name: "ember-leaflet" },
      ],
    });
  },
};
