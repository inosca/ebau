import { module, test } from "qunit";

import {
  cleanTaskAndTemplateFilters,
  addTaskOrTemplateFilter,
} from "ember-ebau-core/utils/work-item-filters";

const TASK = "inquiry";
const TEMPLATE = "0197354f-e981-7142-900e-7f2b41d71d2a";

const FILTERS_BASE = [
  { hasDeadline: true },
  { status: "SUSPENDED" },
  { addressedGroups: ["1"], invert: true },
  { controllingGroups: ["1"] },
  { assignedUsers: ["462afaba-aeb7-494a-8596-3497b81ed701"] },
];

const FILTERS_WITH_TASK = [
  ...FILTERS_BASE,

  { metaValue: [{ key: "not-viewed", value: true }] },
  { task: TASK },
];

const FILTERS_WITH_TEMPLATE = [
  ...FILTERS_BASE,
  {
    metaValue: [
      { key: "not-viewed", value: true },
      { key: "template-id", value: TEMPLATE },
    ],
  },
];

module("Unit | Utility | work-item-filters", function () {
  test("cleans task and template filters", function (assert) {
    assert.deepEqual(cleanTaskAndTemplateFilters(FILTERS_BASE), FILTERS_BASE);
    assert.deepEqual(cleanTaskAndTemplateFilters(FILTERS_WITH_TASK), [
      ...FILTERS_BASE,
      { metaValue: [{ key: "not-viewed", value: true }] },
    ]);
    assert.deepEqual(cleanTaskAndTemplateFilters(FILTERS_WITH_TEMPLATE), [
      ...FILTERS_BASE,
      { metaValue: [{ key: "not-viewed", value: true }] },
    ]);
  });

  test("adds task or template filters", function (assert) {
    assert.deepEqual(
      addTaskOrTemplateFilter(FILTERS_WITH_TEMPLATE, "template", TEMPLATE),
      FILTERS_WITH_TEMPLATE,
    );
    assert.deepEqual(
      addTaskOrTemplateFilter(FILTERS_WITH_TEMPLATE, "task", TASK),
      FILTERS_WITH_TASK,
    );
  });
});
