import { getOwnConfig } from "@embroider/macros";
import Component from "@glimmer/component";

const evenUrl = getOwnConfig().evenUrl;

export default class EvenProjectnumberListComponent extends Component {
  get list() {
    if (this.args.value) {
      const evenNumbers = this.args.value.split(",");
      return evenNumbers.map((item, i) => ({
        label: item.trim() + (i < evenNumbers.length - 1 ? "," : ""),
        url: `${evenUrl}${item.trim()}`,
      }));
    }
    return [];
  }
}
