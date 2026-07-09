import { action } from "@ember/object";
import { service } from "@ember/service";
import { macroCondition, isTesting } from "@embroider/macros";
import Component from "@glimmer/component";
import { task, timeout } from "ember-concurrency";
import { query } from "ember-data-resources";

import { groupAndSort } from "ember-ebau-core/utils/snippets";

export default class SnippetsTable extends Component {
  @service store;
  @service ebauModules;

  snippets = query(this, "notification-template", () => ({
    type: "textcomponent",
    search: this.args.search,
  }));

  get categories() {
    const records = this.snippets.records || [];
    const ownRecords = records.filter(
      (s) => s.service?.id === String(this.ebauModules.serviceId),
    );
    return groupAndSort(ownRecords);
  }

  get globalCategories() {
    const records = this.snippets.records || [];
    const globalRecords = records.filter((s) => s.service?.id === null);

    return groupAndSort(globalRecords);
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
