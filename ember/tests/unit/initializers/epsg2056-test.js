/* global L */
import Application from "@ember/application";
import { run } from "@ember/runloop";

import { initialize } from "citizen-portal/initializers/epsg2056";
import { module, test } from "qunit";
import destroyApp from "../../helpers/destroy-app";

module("Unit | Initializer | epsg2056", function(hooks) {
  hooks.beforeEach(function() {
    run(() => {
      this.application = Application.create();
      this.application.deferReadiness();
    });
  });

  hooks.afterEach(function() {
    destroyApp(this.application);
  });

  test("it works", function(assert) {
    initialize(this.application);

    const latlng = L.latLng([46.947974, 7.447447]); // bern
    const epsg2056 = L.point([2600671.05, 1199654.43]); // bern

    const crs = L.CRS.EPSG2056;

    // we need to round here since epsg2056 is alot preciser than latlng
    assert.equal(
      crs
        .project(latlng)
        .round()
        .toString(),
      epsg2056.round().toString()
    );
    assert.equal(crs.unproject(epsg2056).toString(), latlng.toString());
  });
});
