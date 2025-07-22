import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { query } from "ember-data-resources";

export default class DeadlinesDeadlineDetailComponent extends Component {
  @service abilities;
  @service ebauModules;
  @service store;
  @tracked showModal = false;

  deadlineTypesQuery = query(this, "deadline-type", () => ({
    filter: {},
  }));

  get isLoading() {
    return this.deadlineTypesQuery.isLoading;
  }

  get deadlineTypes() {
    return this.deadlineTypesQuery.records ?? [];
  }

  @action
  reload() {
    // reload instance for case header updates
    this.store.findRecord("instance", this.args.deadline.instance.id);
  }

  @action
  async editDeadline() {
    if (!(await this.abilities.can("edit deadline"))) {
      return;
    }

    this.showModal = true;
  }
}
