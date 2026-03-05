import { service } from "@ember/service";
import Component from "@glimmer/component";
import { query } from "ember-data-resources";

export default class InquiryHintOpenSuspensionsComponent extends Component {
  @service calumaOptions;

  deadlinesQuery = query(this, "instance-deadline", () => ({
    filter: {
      instance: this.calumaOptions.currentInstanceId,
    },
  }));

  get workItemIsReady() {
    return this.args.context.inquiry.status === "READY";
  }

  get isLoading() {
    return this.deadlinesQuery.isLoading;
  }

  get deadline() {
    return (this.deadlinesQuery.records ?? [])[0];
  }

  get deadlineExpired() {
    if (!this.deadline) {
      return false;
    }

    const now = new Date();
    const deadlineDate = this.deadline.targetDeadlineDate;

    return deadlineDate && deadlineDate < now;
  }
}
