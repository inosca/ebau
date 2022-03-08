import { setComponentTemplate } from "@ember/component";
import { ensureSafeComponent } from "@embroider/util";
import Component from "@glimmer/component";

import template from "./template";

import SnippetsComponent from "camac-ng/ui/components/snippets/component";

export class CfSnippetsTextareaComponent extends Component {
  get snippets() {
    return ensureSafeComponent(SnippetsComponent, this);
  }
}

// this is needed so the engine knows of the correct template because we use pods
export default setComponentTemplate(template, CfSnippetsTextareaComponent);
