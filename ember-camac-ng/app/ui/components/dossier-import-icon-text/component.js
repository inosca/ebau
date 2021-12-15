import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";
import Ember from "ember";

export default class DossierImportIconTextComponent extends Component {
  get iconOptions() {
    switch (this.args.status) {
      case "success":
        return "icon: check; ratio: 0.5";
      case "warning":
        return "icon: warning; ratio: 1";
      case "error":
        return "icon: close; ratio: 0.5";
    }

    return null;
  }
}
