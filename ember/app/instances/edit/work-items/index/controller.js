import Controller from "@ember/controller";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";

export default class InstancesEditWorkItemsIndexController extends Controller {
  @calumaQuery({
    query: allWorkItems,
    options: {},
  })
  workItemsQuery;

  @dropTask
  *fetchWorkItems() {
    const filter = [
      { hasDeadline: true },
      {
        rootCaseMetaValue: [
          { key: "camac-instance-id", value: this.model.instance.id },
        ],
      },
      { addressedGroups: ["applicant"] },
    ];

    yield this.workItemsQuery.fetch({
      filter: [...filter],
      order: [
        { attribute: "STATUS", direction: "DESC" },
        { attribute: "DEADLINE", direction: "DESC" },
      ],
    });
  }
}
