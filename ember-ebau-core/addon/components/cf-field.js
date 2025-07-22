import { service } from "@ember/service";
import { ensureSafeComponent } from "@embroider/util";
import Component from "@glimmer/component";
import CfFieldComponent from "@projectcaluma/ember-form/components/cf-field";

export default class CustomCfFieldComponent extends Component {
  @service session;

  get hiddenInternal() {
    return (
      this.args.field.question.raw.meta.hiddenInternal &&
      this.session.isInternal
    );
  }

  get originalComponent() {
    return ensureSafeComponent(CfFieldComponent, this);
  }
}
