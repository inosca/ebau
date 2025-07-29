import { service } from "@ember/service";
import { camelize } from "@ember/string";
import Component from "@glimmer/component";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import BaseQuery from "@projectcaluma/ember-core/caluma-query/queries/base";
import { queryManager } from "ember-apollo-client";
import { query } from "ember-data-resources";
import { gql } from "graphql-tag";
import { trackedFunction } from "reactiveweb/function";
import { validate as isUUID } from "uuid";

import mainConfig from "ember-ebau-core/config/main";
import workItemListConfig from "ember-ebau-core/config/work-item-list";
import taskNamesQuery from "ember-ebau-core/gql/queries/task-names.graphql";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import apolloQuery from "ember-ebau-core/resources/apollo";
import getProcessData, {
  fetchIfNotCached,
} from "ember-ebau-core/utils/work-item";
import { addTaskOrTemplateFilter } from "ember-ebau-core/utils/work-item-filters";

class WorkItemListQuery extends BaseQuery {
  dataKey = "allWorkItems";
  modelName = "work-item";

  constructor(options) {
    super(options);
    this.columns = options.columns;
  }

  // Inlined version of ember-caluma's `allWorkItems`, allowing us
  // to only fetch what is really needed for the work item list.
  get query() {
    const columnSlugs = {
      description: mainConfig.intentSlugs,
      municipality: mainConfig.answerSlugs.municipality,
      applicants: mainConfig.answerSlugs.personalDataApplicant,
    };
    const questions = JSON.stringify(
      this.columns
        .map((col) => columnSlugs[col])
        .filter(Boolean)
        .flat(),
    );
    return `
      query WorkItemListQuery(
        $filter: [WorkItemFilterSetType]
        $order: [WorkItemOrderSetType]
        $cursor: String
        $pageSize: Int
      ) {
        allWorkItems(
          filter: $filter
          order: $order
          after: $cursor
          first: $pageSize
        ) {
          ${this.pagination}
          edges {
            cursor
            node {
              id
              __typename
              ...WorkItemFragment
            }
          }
        }
      }

      fragment WorkItemFragment on WorkItem {
        closedAt
        closedByUser
        status
        meta
        addressedGroups
        controllingGroups
        assignedUsers
        name
        deadline
        task {
          slug
          meta
        }
        case {
          id
          meta
          family {
            id
            meta
            document {
              id
              form {
                name
              }
              answers(filter: [{ questions: ${questions} }]) {
                edges {
                  node {
                    question {
                      id
                      slug
                      ... on TableQuestion {
                        rowForm {
                          slug
                        }
                      }
                    }
                    ... on TableAnswer {
                      value {
                        answers {
                          edges {
                            node {
                              question {
                                slug
                              }
                              ... on StringAnswer {
                                stringValue: value
                              }
                            }
                          }
                        }
                      }
                    }
                    ... on StringAnswer {
                      stringValue: value
                      selectedOption {
                        slug
                        label
                      }
                    }
                  }
                }
              }
            }
          }
          parentWorkItem {
            id
            meta
            addressedGroups
            controllingGroups
            task {
              slug
              meta
            }
            case {
              id
              parentWorkItem {
                id
                task {
                  slug
                }
                childCase {
                  id
                }
              }
            }
            childCase {
              id
            }
          }
        }
      }
    `;
  }
}

export default class WorkItemListWrapperComponent extends Component {
  @queryManager apollo;

  @service store;
  @service calumaOptions;
  @service intl;
  @service ebauModules;

  workItemsQuery = useCalumaQuery(
    this,
    (options) => new WorkItemListQuery(options),
    () => ({
      options: {
        pageSize: workItemListConfig.pageSize || 20,
        processNew: (workItems) => this.processNew(workItems),
        columns: this.columns,
      },
      filter: this.gqlFilter,
      order: this.gqlOrder,
    }),
  );

  workItemListConfig = workItemListConfig;

  get columns() {
    return workItemListConfig.columns(
      this.args.status,
      this.ebauModules.baseRole,
    );
  }

  async processNew(workItems) {
    const { usernames, serviceIds, instanceIds } = getProcessData(workItems);

    if (instanceIds.length && this.args.application === "kt_schwyz") {
      // only Kt. SZ needs to fetch instances for the global work item list!
      // also, we don't wait before any of the requests to complete to get a
      // faster first render. Only exception is the instance call (to avoid many more
      // api calls being triggered by ember-data)
      await fetchIfNotCached(
        this.store,
        "instance",
        instanceIds,
        "id",
        "instance_id",
        {
          include: "form",
        },
      );
      this.store.query("form-field", {
        instance: instanceIds.join(","),
        name: "bezeichnung,bezeichnung-override",
      });
    }

    if (hasFeature("workItemList.useColorForNFD")) {
      await fetchIfNotCached(
        this.store,
        "instance",
        instanceIds,
        "id",
        "instance_id",
        {
          "fields[instances]": "id,instance_state",
        },
      );
    }

    fetchIfNotCached(this.store, "service", serviceIds, "id", "service_id");
    const allUsernames = [...new Set(usernames, this.args.username)];
    fetchIfNotCached(
      this.store,
      "public-user",
      allUsernames,
      "username",
      "username",
    );

    return workItems;
  }

  get gqlTaskFilter() {
    if (this.args.task === "all") {
      const emptyFilters = [];

      if (this.preset?.prefilterTasks) {
        emptyFilters.push({ tasks: this.preset.excludedTasks, invert: true });
      }

      if (this.preset?.prefilterWorkItemTemplates) {
        emptyFilters.push({
          metaValue: [
            {
              key: "template-id",
              value: [...this.preset.excludedWorkItemTemplates, "NONE"],
              lookup: "IN",
            },
          ],
          invert: true,
        });
      }

      return emptyFilters;
    }

    if (isUUID(this.args.task)) {
      return [{ metaValue: [{ key: "template-id", value: this.args.task }] }];
    }

    return [{ task: this.args.task }];
  }

  get gqlFilter() {
    return [
      { hasDeadline: true },
      { status: this.args.status },
      {
        addressedGroups: [String(this.args.serviceId)],
        invert: this.args.role === "control",
      },
      ...(this.args.role === "control"
        ? [{ controllingGroups: [String(this.args.serviceId)] }]
        : []),
      ...(this.args.responsible === "own"
        ? [{ assignedUsers: [this.args.username] }]
        : []),
      ...(!["own", "all"].includes(this.args.responsible)
        ? [{ assignedUsers: [this.args.responsible] }]
        : []),
      ...(this.args.type === "unread"
        ? [{ metaValue: [{ key: "not-viewed", value: true }] }]
        : []),
      ...this.gqlTaskFilter,
      ...(hasFeature("workItems.hideImportedWorkItems")
        ? [{ metaValue: [{ key: "imported", value: true }], invert: true }]
        : []),
    ];
  }

  get gqlOrder() {
    return this.args.order === "urgent"
      ? [{ attribute: "DEADLINE", direction: "ASC" }]
      : [{ attribute: "CREATED_AT", direction: "DESC" }];
  }

  get _taskSlugs() {
    if (!workItemListConfig.showTaskFilter) {
      return [];
    }

    const availableTasks = workItemListConfig.availableTasks;

    let tasks = [
      ...(availableTasks.roles?.[this.args.baseRole] ?? []),
      ...(availableTasks.serviceGroups?.[this.args.serviceGroupSlug] ?? []),
      ...(availableTasks.services?.[this.args.serviceId] ?? []),
      ...(availableTasks.default ?? []),
    ];

    if (this.args.preset) {
      const presetTasks = this.preset?.tasks;
      if (this.preset?.prefilterTasks) {
        tasks = tasks.filter((task) => presetTasks.includes(task));
      }
    }

    const templates = availableTasks.includeTemplates
      ? this.workItemTemplates.records?.map((tpl) => tpl.id)
      : [];

    return [
      ...tasks.map((slug) => ({
        slug,
        gqlAlias: camelize(slug),
        type: "task",
      })),
      ...templates.map((slug, i) => ({
        slug,
        gqlAlias: `template${i + 1}`,
        type: "template",
      })),
    ];
  }

  allResponsibles = trackedFunction(this, async () => {
    const users = await this.store.query("user", {
      sort: "name",
    });
    return [
      { value: "all", label: this.intl.t("workItems.filters.all") },
      { value: "own", label: this.intl.t("workItems.filters.own") },
      ...users.map((u) => ({
        label: `${u.name} ${u.surname}`,
        value: u.username,
      })),
    ];
  });

  taskNames = apolloQuery(
    this,
    () => ({
      query: taskNamesQuery,
      variables: {
        tasks: this._taskSlugs
          .filter(({ type }) => type === "task")
          .map(({ slug }) => slug),
      },
    }),
    "allTasks.edges",
    (data) =>
      data.reduce((obj, { node }) => {
        return { ...obj, [node.slug]: node.name };
      }, {}),
  );

  workItemTemplates = query(this, "work-item-template", () => ({
    ...(this.args.preset ? { included_in_preset: this.args.preset } : {}),
  }));

  get preset() {
    const allPresets = this.store.peekAll("work-item-list-filter-preset");

    return allPresets.find((preset) => preset.id === this.args.preset);
  }

  availableTasks = trackedFunction(this, async () => {
    if (!this.workItemsQuery.value || this._taskSlugs.length === 0) {
      return [];
    }

    /* In order to avoid having 1 request per task filter btn we do a single query.
      However, as we have a dynamic number of tasks and we need to use the task slug in the filter
      we need to build the query dynamically. The code below will generate graphql query like this:

      query WorkItemsForTasks {
        myFirstTask: allTasks(filter: [{ hasDeadline: true }, .... { task: "my-first-task" }]) {
          totalCount
        }
        mySecondTask: allTasks(filter: [{ hasDeadline: true }, .... { task: "my-second-task" }]) {
          totalCount
        }
      }
    */

    const body = this._taskSlugs
      .map(({ slug, gqlAlias, type }) => {
        const filters = addTaskOrTemplateFilter(this.gqlFilter, type, slug);

        // The weird string stuff and replacement stuff is required because of the differences between JSON and GraphQL
        // such as graphql enums, etc.
        return `${gqlAlias}: allWorkItems(filter: ${JSON.stringify(filters)
          .replace(/"(\w+)":/g, "$1:")
          .replace(/"SUSPENDED"/g, "SUSPENDED")
          .replace(/"COMPLETED"/g, "COMPLETED")
          .replace(/"READY"/g, "READY")}) {
          totalCount
        }`;
      })
      .join("\n");

    const query = gql`
      query WorkItemsForTasks {
        ${body}
      }
    `;

    // Trigger loading of task names in order to avoid UI flickering
    this.taskNames.value;

    const allTasks = await this.apollo.query({ query });

    // Prepare options for select
    return [
      { value: "all", label: this.intl.t("workItems.filters.all") },
      ...this._taskSlugs.map(({ slug, type, gqlAlias }) => {
        const labelKey = `workItems.filters.task.${slug}`;
        let taskName;

        if (type === "task") {
          // By default, the task names are taken from the actual task models via
          // GraphQL. However, in UR there are some cases where they wanted a
          // different task name in the filter which is why we allow for an
          // override here.
          taskName = this.intl.exists(labelKey)
            ? this.intl.t(labelKey)
            : this.taskNames.value?.[slug];
        } else if (type === "template") {
          taskName = this.store.peekRecord("work-item-template", slug).name;
        }

        return {
          label: this.intl.t("workItems.filters.task.generic", {
            taskName,
            count: allTasks[gqlAlias]?.totalCount ?? 0,
            htmlSafe: true,
          }),
          value: slug,
        };
      }),
    ];
  });
}
