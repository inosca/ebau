import Component from "@glimmer/component";
import mainConfig from "ember-ebau-core/config/main";

export default class EvenOverviewGridCellComponent extends Component {
  get url() {
    if (this.args.value && mainConfig.even.projectUrl) {
      return `${mainConfig.even.projectUrl}${this.args.value}`;
    }
    return null;
  }
}
