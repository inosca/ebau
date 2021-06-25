import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class PersonalSuggestionsEntryComponent extends Component {
  get name() {
    return (
      this.args.person.juristicName ||
      `${this.args.person.firstName} ${this.args.person.lastName}`
    );
  }

  @action select(email, event) {
    event.preventDefault();

    this.args.onSelect?.(email);
  }
}
