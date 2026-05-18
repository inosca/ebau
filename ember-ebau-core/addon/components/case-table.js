import { service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import { getOwnConfig, macroCondition } from "@embroider/macros";
import Component from "@glimmer/component";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";

import caseTableConfig from "ember-ebau-core/config/case-table";
import caseInstanceIdsQuery from "ember-ebau-core/gql/queries/case-instance-ids.graphql";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import {
  getCalumaFilters,
  getCamacFilters,
} from "ember-ebau-core/utils/case-filters";

export default class CaseTableComponent extends Component {
  @service store;
  @service intl;
  @service fetch;
  @service notification;
  @service router;
  @service ebauModules;
  @service permissions;

  @queryManager apollo;

  casesQuery = useCalumaQuery(this, allCases, () => ({
    options: {
      pageSize: caseTableConfig.pageSize || 15,
      processNew: (cases) => this.processNew(cases),
    },
    ...this.gqlOrder,
    filter: this.gqlFilter,
    queryOptions: {
      context: {
        headers: {
          ...this.camacFilter,
          ...this.camacOrder,
        },
      },
    },
  }));

  get showEntries() {
    if (!this.ebauModules.isSupportRole) {
      return true;
    }

    return Object.values(this.args.filter).some((filter) => !isEmpty(filter));
  }

  get isService() {
    return this.ebauModules.baseRole === "service";
  }

  get order() {
    const config =
      caseTableConfig.availableOrderings[this.args.order.replace(/^-/, "")];
    const direction = this.args.order.startsWith("-") ? "ASC" : "DESC";

    if (
      Object.keys(config).includes("caluma") &&
      Object.keys(config).includes("camac-ng")
    ) {
      return {
        [this.args.casesBackend]: config[this.args.casesBackend],
        direction,
      };
    }

    return { ...config, direction };
  }

  get gqlOrder() {
    const config = this.order.caluma;

    return config
      ? {
          order: config.map((orderConfig) => ({
            ...orderConfig,
            direction: orderConfig.direction ?? this.order.direction,
          })),
        }
      : {};
  }

  get camacOrder() {
    const config = this.order["camac-ng"];
    const inverted = this.order.direction === "DESC";

    return config
      ? {
          "x-camac-order": config
            .map((order) => `${inverted ? "-" : ""}${order}`)
            .join(","),
        }
      : {};
  }

  get gqlFilter() {
    const filter = this.args.filter;
    const availableFilterSet = getCalumaFilters(
      this.args.filter,
      this.args.casesBackend,
    );

    const searchFilters = Object.entries(filter)
      .filter(
        ([key, value]) => Boolean(value) && Boolean(availableFilterSet[key]),
      )
      .map(([key]) => availableFilterSet[key]);

    const workflow = this.args.workflow;
    const excludeWorkflow = this.args.excludeWorkflow;
    return [
      { excludeChildCases: true },
      { metaHasKey: "camac-instance-id" },
      ...searchFilters,
      ...(workflow ? [{ workflow }] : []),
      ...(excludeWorkflow ? [{ workflow: excludeWorkflow, invert: true }] : []),
    ];
  }

  get camacFilter() {
    const filters = getCamacFilters(this.args);
    return {
      "x-camac-filters": Object.entries(filters)
        .filter(([, value]) => ![null, undefined, ""].includes(value))
        .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
        .join("&"),
    };
  }

  async processNew(cases) {
    if (!cases.length) {
      return [];
    }

    const instanceIds = cases.map((_case) => _case.meta["camac-instance-id"]);

    if (macroCondition(getOwnConfig().application === "ur")) {
      if (this.isService) {
        await this.store.query("responsible-service", {
          include: "responsible_user",
          instance: instanceIds.join(","),
        });
      }
    }

    await this.store.query("instance", {
      instance_id: instanceIds.join(","),
      include: [
        "instance_state",
        ...(macroCondition(getOwnConfig().application === "ur")
          ? ["user"]
          : []),
        ...(macroCondition(getOwnConfig().application === "sz")
          ? ["form", "user"]
          : []),
        ...(hasFeature("instanceMarks") ? ["instance_marks"] : []),
      ].join(","),
      ...(macroCondition(getOwnConfig().application === "be")
        ? {
            "fields[instances]":
              "id,name,decision,decision_date,involved_at,instance_state,is_paper,ebau_number",
          }
        : {}),
      ...(macroCondition(getOwnConfig().application === "gr")
        ? {
            "fields[instances]": "id,name,decision,instance_state,involved_at",
          }
        : {}),
      ...(macroCondition(getOwnConfig().application === "so")
        ? {
            "fields[instances]": "id,name,decision,instance_state,is_paper",
          }
        : {}),
    });

    if (this.args.casesBackend === "camac-ng") {
      await this.store.query("form-field", {
        instance: instanceIds.join(","),
        name: (caseTableConfig.formFields ?? []).join(","),
        include: "instance",
      });
    }

    return cases;
  }

  get tableColumns() {
    const tableColumns = caseTableConfig.columns[this.args.casesBackend];

    const columnNames = Array.isArray(tableColumns)
      ? tableColumns
      : (tableColumns[this.ebauModules.baseRole] ?? tableColumns.default ?? []);

    const availableOrderings = Object.keys(
      caseTableConfig.availableOrderings ?? [],
    );

    return columnNames.map((name) => ({
      name,
      order: availableOrderings.find((ordering) => ordering === name),
    }));
  }

  @dropTask
  *export(event) {
    event.preventDefault();

    try {
      if (this.casesQuery.totalCount > 1000) {
        this.notification.danger(this.intl.t("cases.export.too-many"));
        return;
      }

      const response = yield this.apollo.query(
        {
          query: caseInstanceIdsQuery,
          fetchPolicy: "network-only",
          variables: { filter: this.gqlFilter },
          context: {
            headers: this.camacFilter,
          },
        },
        "allCases.edges",
      );

      const ids = response.map((edge) => edge.node.meta["camac-instance-id"]);

      const exportResponse = yield this.fetch.fetch(
        `/api/v1/instances/export?instance_id=${ids.join(",")}`,
      );

      saveAs(yield exportResponse.blob(), "export.xlsx");
    } catch {
      this.notification.danger(this.intl.t("cases.export.error"));
    }
  }
}
