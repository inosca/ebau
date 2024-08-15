import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import mainConfig from "ember-ebau-core/config/main";

export default class StateInfoButtonComponent extends Component {
  @tracked showModal = false;

  publicInstanceStates = mainConfig.publicInstanceStates;

  @action
  async toggle(event) {
    event.preventDefault();

    this.showModal = !this.showModal;
  }
}
