import { ensureSafeComponent } from "@embroider/util";
import Component from "@glimmer/component";
import SnippetsComponent from "ember-ebau-core/components/snippets";

export default class CfSnippetsTextareaComponent extends Component {
  get snippets() {
    return ensureSafeComponent(SnippetsComponent, this);
  }
}
