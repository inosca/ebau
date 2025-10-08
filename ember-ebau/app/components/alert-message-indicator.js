import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { query } from "ember-data-resources";

export default class AlertMessageIndicatorComponent extends Component {
  @service("alert-messages") alertMessages;

  @tracked showModal = false;

  query = query(this, "alert-message", () => ({}));

  get messages() {
    return this.query.records ?? [];
  }

  get count() {
    return this.messages.length;
  }

  @action
  showAlertMessages() {
    this.showModal = true;
  }

  @action
  hideModal() {
    this.showModal = false;
  }
}
