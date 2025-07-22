import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { query } from "ember-data-resources";

export default class DeadlinesOverviewComponent extends Component {
  @service ebauModules;

  deadlinesQuery = query(this, "instance-deadline", () => ({
    filter: {
      instance: this.ebauModules.instanceId,
    },
  }));

  get isLoading() {
    return this.deadlineTypesQuery.isLoading || this.deadlinesQuery.isLoading;
  }

  get deadline() {
    return (this.deadlinesQuery.records ?? [])[0];
  }

  @action
  reload() {
    this.deadlinesQuery.retry();
  }
}
