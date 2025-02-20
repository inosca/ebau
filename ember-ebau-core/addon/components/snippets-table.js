import { action } from "@ember/object";
import { service } from "@ember/service";
import { macroCondition, isTesting } from "@embroider/macros";
import Component from "@glimmer/component";
import { task, timeout } from "ember-concurrency";
import { query } from "ember-data-resources";

export default class SnippetsTable extends Component {
  @service store;

  snippets = query(this, "notification-template", () => ({
    type: "textcomponent",
    search: this.args.search,
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

  onSearch = task({ restartable: true }, async (event) => {
    if (macroCondition(!isTesting())) {
      await timeout(500);
    }

    this.args.onUpdateSearch?.(event.target.value);
  });
}
