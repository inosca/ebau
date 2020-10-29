import { action } from "@ember/object";
import { later, cancel } from "@ember/runloop";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class ContextMenuComponent extends Component {
  @tracked menuOpen = false;
  closeMenuDelay;

  @action
  handleMouseLeave() {
    this.closeMenuDelay = later(
      this,
      function () {
        this.menuOpen = false;
      },
      1000
    );
  }

  @action
  handleMouseEnter() {
    cancel(this.closeMenuDelay);
  }
}
