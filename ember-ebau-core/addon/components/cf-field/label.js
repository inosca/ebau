import { service } from "@ember/service";
import { getOwnConfig } from "@embroider/macros";
import { ensureSafeComponent } from "@embroider/util";
import Component from "@glimmer/component";
import CfInputLabelComponent from "@projectcaluma/ember-form/components/cf-field/label";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class CustomCfFieldLabelComponent extends Component {
  @service intl;

  get originalLabel() {
    return ensureSafeComponent(CfInputLabelComponent, this);
  }

  get gisChanges() {
    if (!hasFeature("gis.showChanges")) {
      return null;
    }

    const gisValue = this.args.field.answer.raw.meta?.["gis-value"];
    const value = this.args.field.answer.serializedValue;

    if (
      gisValue === undefined ||
      JSON.stringify(value) === JSON.stringify(gisValue)
    ) {
      return null;
    }

    if (this.args.field.questionType === "TableQuestion") {
      const added = value.filter((id) => !gisValue.includes(id)).length;
      const removed = gisValue.filter((id) => !value.includes(id)).length;

      return {
        new:
          added > 0
            ? this.intl.t("gis.changes.row-added", { count: added })
            : null,
        old:
          removed > 0
            ? this.intl.t("gis.changes.row-removed", { count: removed })
            : null,
      };
    }

    return {
      new: value,
      old: gisValue,
    };
  }

  get gisLink() {
    try {
      const layers = this.args.field.question.raw.meta["gis-layers"];

      if (!layers) {
        return null;
      }

      const plot = this.args.field.document.findAnswer("parzellen")?.[0];
      const x = plot?.["lagekoordinaten-ost"];
      const y = plot?.["lagekoordinaten-nord"];

      const query = [
        "bl=hintergrundkarte_sw",
        "s=1000",
        `l=${layers.join(",")}`,
        x && y ? `c=${x},${y}` : null,
      ]
        .filter(Boolean)
        .join("&");

      return `${getOwnConfig().soGisUrl}/map/?${query}`;
    } catch {
      return null;
    }
  }
}
