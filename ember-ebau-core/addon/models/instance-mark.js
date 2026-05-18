import { htmlSafe } from "@ember/template";
import { attr, hasMany } from "@ember-data/model";
import { LocalizedModel, localizedAttr } from "ember-localized-model";

export default class InstanceMarkModel extends LocalizedModel {
  @localizedAttr name;
  @attr icon;
  @attr backgroundColor;
  @attr textColor;
  @attr sort;

  @hasMany("instance", { inverse: "instanceMarks", async: true }) instances;

  get style() {
    return htmlSafe(
      `background-color: ${this.backgroundColor}; color: ${this.textColor};`,
    );
  }
  get iconStyle() {
    return htmlSafe(`color: ${this.backgroundColor}`);
  }
}
