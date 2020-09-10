import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class ContextMenuComponent extends Component {
  @tracked menuOpen = false;
}
