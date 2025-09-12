import Component from "@glimmer/component";

import mainConfig from "ember-ebau-core/config/main";

export default class EvenProjectnumberListComponent extends Component {
  get list() {
    if (this.args.value) {
      const evenNumbers = this.args.value.split(",");
      return evenNumbers.map((item, i) => ({
        label: item.trim() + (i < evenNumbers.length - 1 ? "," : ""),
        url: `${mainConfig.even.projectUrl}${item.trim()}`,
      }));
    }
    return [];
  }
}
