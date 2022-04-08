import Component from "@glimmer/component";

export default class WorkItemListWrapperComponent extends Component {
  // for testing
  get workItems() {
    return [];
  }

  get columns() {
    return [
      "task",
      "instance",
      "description",
      ...(this.status === "open"
        ? ["deadline", "responsible"]
        : ["closedAt", "closedBy"]),
    ];
  }
}
