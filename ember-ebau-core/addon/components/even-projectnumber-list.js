import { getOwnConfig } from "@embroider/macros";
import Component from "@glimmer/component";

export default class EvenProjectnumberListComponent extends Component {
  get list() {
    if (this.args.value) {
      const url = this.evenUrl.endsWith("/")
        ? this.evenUrl.slice(0, -1)
        : this.evenUrl;
      const evenNumbers = this.args.value.split(",");
      return evenNumbers.map((item, i) => ({
        label: item.trim() + (i < evenNumbers.length - 1 ? "," : ""),
        url: `${url}/${item.trim()}`,
      }));
    }
    return [];
  }

  get evenUrl() {
    return getOwnConfig().evenUrl;
  }
}
