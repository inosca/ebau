import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CommunicationMessageListComponent extends Component {
  @action
  scrollIntoView(index, element) {
    // Scroll last message automatically into view
    if (this.args.messages.length === index + 1) {
      element.scrollIntoView();
    }
  }
}
