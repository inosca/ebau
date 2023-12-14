import { visit, click } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";
import { test } from "dummy/tests/helpers/scenarios";

module("Acceptance | workitem-list", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    this.workItemsTask1 = this.server.createList("workItem", 3, {
      addressedGroups: ["1"],
      status: "READY",
      hasDeadline: true,
      task: this.server.create("task", {
        name: "task-1",
        slug: "task-1",
      }),
    });
    this.workItemsTask2 = this.server.createList("workItem", 3, {
      addressedGroups: ["1"],
      status: "READY",
      hasDeadline: true,
      task: this.server.create("task", {
        name: "task-2",
        slug: "task-2",
      }),
    });
  });

  test("can filter by task", async function (assert) {
    await visit("/work-items");

    const containsWorkItemLabels = function (workItems) {
      workItems.forEach((workItem) => {
        assert.dom("[data-test-work-item-list]").containsText(workItem.name);
      });
    };
    const doesNotcontainsWorkItemLabels = function (workItems) {
      workItems.forEach((workItem) => {
        assert
          .dom("[data-test-work-item-list]")
          .doesNotContainText(workItem.name);
      });
    };

    // show all tasks
    await click("[data-test-task-radio] div button:nth-child(1)");
    assert.dom("[data-test-work-item-list] tbody tr").exists({ count: 6 });
    containsWorkItemLabels(this.workItemsTask1);
    containsWorkItemLabels(this.workItemsTask2);

    // filter by first task
    await click("[data-test-task-radio] div button:nth-child(2)");
    assert.dom("[data-test-work-item-list] tbody tr").exists({ count: 3 });
    containsWorkItemLabels(this.workItemsTask1);
    doesNotcontainsWorkItemLabels(this.workItemsTask2);

    // filter by second task
    await click("[data-test-task-radio] div button:nth-child(3)");
    assert.dom("[data-test-work-item-list] tbody tr").exists({ count: 3 });
    containsWorkItemLabels(this.workItemsTask2);
    doesNotcontainsWorkItemLabels(this.workItemsTask1);
  });
});
