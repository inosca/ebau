import { service } from "@ember/service";
import { camelize } from "@ember/string";
import Component from "@glimmer/component";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import BaseQuery from "@projectcaluma/ember-core/caluma-query/queries/base";
import { queryManager } from "ember-apollo-client";
import { gql } from "graphql-tag";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";
import workItemListConfig from "ember-ebau-core/config/work-item-list";
import getProcessData, {
  fetchIfNotCached,
} from "ember-ebau-core/utils/work-item";

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
      ...(this.args.task !== "all" ? [{ task: this.args.task }] : []),
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

    return [
      ...(availableTasks.roles[this.args.baseRole] ?? []),
      ...(availableTasks.services[this.args.serviceId] ?? []),
      ...(availableTasks.default ?? []),
    ];
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
      .map(camelize)
      .map((snakeCaseTaskSlug, i) => {
        const filters = [...this.gqlFilter];
        const existingTaskFilter = filters.find((filter) => filter.task);

        if (existingTaskFilter) {
          existingTaskFilter.task = this._taskSlugs[i];
        } else {
          filters.push({ task: this._taskSlugs[i] });
        }

        // The weird string stuff and replacement stuff is required because of the differences between JSON and GraphQL
        // such as graphql enums, etc.
        return `${snakeCaseTaskSlug}: allWorkItems(filter: ${JSON.stringify(
          filters,
        )
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

    const allTasks = await this.apollo.query({
      query,
    });

    return [
      { value: "all", label: this.intl.t("workItems.filters.all") },
      ...Object.keys(allTasks).map((task, i) => ({
        label: this.intl.t(`workItems.filters.task.${this._taskSlugs[i]}`, {
          count: allTasks[task].totalCount,
          htmlSafe: true,
        }),
        value: this._taskSlugs[i],
      })), // prepare options for select
    ];
  });
}
