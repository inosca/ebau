import { action } from "@ember/object";
import Component from "@glimmer/component";
import { findAll } from "ember-data-resources";
import { localCopy } from "tracked-toolbox";

export default class InstanceMarkEditorComponent extends Component {
  @localCopy("args.selectedMarks") selectedMarks;

  allMarks = findAll(this, "instance-mark", () => ({}));

  @action
  selectMark(mark, event) {
    event?.preventDefault();

    const set = new Set(this.selectedMarks.slice());

    if (set.has(mark)) {
      set.delete(mark);
    } else {
      set.add(mark);
    }

    this.selectedMarks = [...set];
    this.args.onChange?.(this.selectedMarks);
  }
}
