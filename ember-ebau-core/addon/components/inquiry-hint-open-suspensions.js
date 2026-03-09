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

  suspensionsQuery = query(this, "suspension", () => {
    if (!this.deadline?.id) {
      return null;
    }

    return {
      filter: {
        deadline: this.deadline.id,
      },
      include: "deadline",
    };
  });

  get workItemIsReady() {
    return this.args.context.inquiry.status === "READY";
  }

  get isLoading() {
    return this.deadlinesQuery.isLoading || this.suspensionsQuery.isLoading;
  }

  get deadline() {
    return (this.deadlinesQuery.records ?? [])[0];
  }

  get openSuspensions() {
    return (this.suspensionsQuery.records ?? []).filter(
      (suspension) => !suspension.endDate,
    );
  }
}
