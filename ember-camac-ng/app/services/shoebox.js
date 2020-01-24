import { getOwner } from "@ember/application";
import Service from "@ember/service";

export default class ShoeboxService extends Service {
  get content() {
    const shoebox = getOwner(this)
      .lookup("service:-document")
      .querySelector("#ember-camac-ng-shoebox");

    try {
      return JSON.parse(shoebox.innerHTML);
    } catch (error) {
      return {};
    }
  }
}
