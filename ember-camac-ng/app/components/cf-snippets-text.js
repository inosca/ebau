import { ensureSafeComponent } from "@embroider/util";
import Component from "@glimmer/component";

import SnippetsComponent from "camac-ng/components/snippets";

export default class CfSnippetsTextComponent extends Component {
  get snippets() {
    return ensureSafeComponent(SnippetsComponent, this);
  }
}
