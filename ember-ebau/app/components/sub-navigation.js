import Component from "@glimmer/component";
import { query } from "ember-data-resources";

export default class SubNavigationComponent extends Component {
  instanceResources = query(this, "instance-resource", () => ({
    instance: this.args.instanceId,
  }));
}
