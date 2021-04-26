"use strict";

module.exports = {
  normalizeEntityName() {}, // no-op since we're just adding dependencies

  afterInstall() {
    return this.addAddonsToProject({
      packages: [
        { name: "ember-apollo-client" },
        { name: "ember-caluma" },
        { name: "ember-leaflet" },
      ],
    });
  },
};
