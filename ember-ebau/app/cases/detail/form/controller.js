import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import { trackedFunction } from "reactiveweb/function";

import getInstanceCaseQuery from "ebau/gql/queries/get-instance-case.graphql";

export default class CasesDetailFormController extends Controller {
  @service store;
  @service ebauModules;

  queryParams = ["displayedForm", "timelineId"];

  @tracked displayedForm = "";
  @tracked timelineId = "current";

  @queryManager apollo;

  get compareContext() {
    if (this.isCurrentTimeline) {
      return null;
    }

    return {
      from: this.timeline.startDate,
      to: this.timeline.endDate,
    };
  }

  get isCurrentTimeline() {
    return this.timeline.id === "current";
  }

  formTimelines = trackedFunction(this, async () => {
    if (!hasFeature("corrections.applicantCorrection")) {
      return [];
    }

    const timelines = [
      {
        id: "current",
        timelineType: "current",
        label: "current",
        startDate: null,
        endDate: null,
      },
      ...(await this.store.query("form-timeline", {
        instance: this.ebauModules.instanceId,
      })),
    ];

    return timelines;
  });

  document = trackedFunction(this, async () => {
    const raw = await this.apollo.query(
      {
        query: getInstanceCaseQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.model.id },
      },
      "allCases.edges",
    );

    return raw[0].node.document;
  });

  get timeline() {
    return (this.formTimelines.value ?? []).find(
      (t) => t.id === this.timelineId,
    );
  }

  @action
  changeTimeline(timeline) {
    this.timelineId = timeline.id;
  }
}
