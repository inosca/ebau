import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { query } from "ember-data-resources";

export default class SnippetsTable extends Component {
  @service store;

  snippets = query(this, "notification-template", () => ({
    type: "textcomponent",
  }));

  get categories() {
    const categories = new Set(this.snippets.records?.map((s) => s.purpose));

    return [...categories].toSorted().reduce((grouped, category) => {
      return {
        ...grouped,
        [category]: this.snippets.records
          .filter((s) => s.purpose === category)
          .toSorted((a, b) => a.subject.localeCompare(b.subject)),
      };
    }, {});
  }

  @action
  async refresh() {
    await this.snippets.retry();
  }
}
