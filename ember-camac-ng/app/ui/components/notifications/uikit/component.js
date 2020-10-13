import Component from "@glimmer/component";

export default class NotificationsUikitComponent extends Component {
  get type() {
    const type = this.args.notification.type || "default";

    if (type === "error") {
      return "danger";
    }

    return type;
  }
}
