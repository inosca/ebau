import { setComponentTemplate } from "@ember/component";

import template from "./template";

import { CaseFilterSelectMultipleComponent } from "camac-ng/ui/components/case-filter/select-multiple/component";

export class CaseFilterAsyncSelectMultipleComponent extends CaseFilterSelectMultipleComponent {}

export default setComponentTemplate(
  template,
  CaseFilterAsyncSelectMultipleComponent
);
