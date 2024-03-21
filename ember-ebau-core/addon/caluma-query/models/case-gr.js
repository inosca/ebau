import { inject as service } from "@ember/service";

import CustomCaseBaseModel from "ember-ebau-core/caluma-query/models/-case";
import mainConfig from "ember-ebau-core/config/main";
import { getAnswer } from "ember-ebau-core/utils/get-answer";
import { EPSG2056toLatLng, getCenter } from "ember-ebau-core/utils/gis";

export default class CustomCaseModel extends CustomCaseBaseModel {
  @service intl;
  get centerCoordinate() {
    try {
      const answer = JSON.parse(
        getAnswer(this.raw.document, mainConfig.answerSlugs.coordinates).node
          .stringValue,
      );
      const markers = answer.markers.map((marker) =>
        EPSG2056toLatLng([marker.x, marker.y]),
      );
      return getCenter(markers, answer.geometry);
    } catch (e) {
      console.warn("could not compute center coordinate", e);
      return null;
    }
  }

  get coordinatesLink() {
    if (!this.centerCoordinate) {
      return "";
    }

    return this.intl.t("gis.coordinatesLink", {
      x: this.centerCoordinate.x,
      y: this.centerCoordinate.y,
    });
  }
}
