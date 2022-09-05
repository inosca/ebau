import { setComponentTemplate } from "@ember/component";
import Component from "@glimmer/component";

import template from "./template";

// eslint-disable-next-line ember/no-empty-glimmer-component-classes
export class CaseFilterInputComponent extends Component {}

export default setComponentTemplate(template, CaseFilterInputComponent);
