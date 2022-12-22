import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import { getOwnConfig } from "@embroider/macros";
import { tracked } from "@glimmer/tracking";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";
import { DateTime } from "luxon";
import { cached } from "tracked-toolbox";

import config from "caluma-portal/config/environment";
import trackedFilter from "caluma-portal/decorators/tracked-filter";
import getRootFormsQuery from "caluma-portal/gql/queries/get-root-forms.graphql";

const { answerSlugs } = config.APPLICATION;

const getRecursiveSources = (form, forms) => {
  if (!form.source?.slug) {
    return [];
  }

  const source = forms.find((edge) => edge.node.slug === form.source.slug);

  return [source.node.slug, ...getRecursiveSources(source.node, forms)];
};

const dateFilter = {
  serialize(value) {
    const date = DateTime.fromJSDate(value);

    return date.isValid ? date.toISODate() : null;
  },
  deserialize(value) {
    const date = DateTime.fromISO(value);

    return date.isValid ? date.toJSDate() : null;
  },
};

export default class InstancesIndexController extends Controller {
  @queryManager apollo;

  @service intl;
  @service session;
  @service store;

  @cached
  get queryParams() {
    return [
      "order",
      "category",
      ...this._filtersConfig.map(({ privateKey, publicKey }) => ({
        [privateKey]: publicKey,
      })),
    ];
  }

  @tracked order = "camac-instance-id:desc";
  @tracked category = config.APPLICATION.defaultInstanceStateCategory;

  @trackedFilter({
    serialize(value) {
      return String(value.flatMap((form) => form.value));
    },
    deserialize(value) {
      return this.forms.filter((form) =>
        form.value.some((v) => value.split(",").includes(v))
      );
    },
    defaultValue: "",
  })
  types;

  @trackedFilter({ defaultValue: "" }) instanceId;
  @trackedFilter({ defaultValue: "" }) specialId;
  @trackedFilter({ defaultValue: "" }) parcel;
  @trackedFilter({ defaultValue: "" }) address;
  @trackedFilter({ defaultValue: "" }) applicant;
  @trackedFilter({ ...dateFilter, defaultValue: null }) submitFrom;
  @trackedFilter({ ...dateFilter, defaultValue: null }) submitTo;
  @trackedFilter({ defaultValue: getOwnConfig().instancePaperFilterDefault })
  onlyPaper;

  cases = useCalumaQuery(this, allCases, () => ({
    options: {
      pageSize: 15,
      processNew: (cases) => this.processNew(cases),
    },
    order: this.serializedOrder,
    filter: this.serializedFilter,
    queryOptions: {
      context: {
        headers: this.serializedHeaders,
      },
    },
  }));

  rootForms = trackedTask(this, this.fetchRootForms, () => {});

  get categories() {
    return Object.keys(config.APPLICATION.instanceStateCategories);
  }

  get orderOptions() {
    return [
      {
        value: "camac-instance-id:desc",
        label: "instances.instance-id",
        direction: "instances.desc",
      },
      {
        value: "camac-instance-id:asc",
        label: "instances.instance-id",
        direction: "instances.asc",
      },
      {
        value: `${answerSlugs.specialId}:desc`,
        label: "instances.special-id",
        direction: "instances.desc",
      },
      {
        value: `${answerSlugs.specialId}:asc`,
        label: "instances.special-id",
        direction: "instances.asc",
      },
      {
        value: "submit-date:desc",
        label: "instances.submitDate",
        direction: "instances.desc",
      },
      {
        value: "submit-date:asc",
        label: "instances.submitDate",
        direction: "instances.asc",
      },
    ];
  }

  get allForms() {
    return (this.rootForms.value ?? []).map((edge) => edge.node.slug);
  }

  get formFilterOptions() {
    const categories = [
      "preliminary-clarification",
      "building-permit",
      "special-procedure",
      "others",
    ];

    return categories
      .map((category) => {
        const options = this.forms
          .filter((form) => form.category === category)
          .sort((a, b) => a.order - b.order);

        return options.length
          ? {
              groupName: this.intl.t(`instances.new.${category}.title`),
              options,
            }
          : null;
      })
      .filter(Boolean);
  }

  get forms() {
    const permissions = config.APPLICATION.formCreationPermissions.filter(
      (perm) =>
        perm.roles.includes(parseInt(this.session.group?.role.get("id"))) ||
        (perm.roles.includes("internal") && this.session.isInternal) ||
        (perm.roles.includes("public") && !this.session.isInternal)
    );
    const raw = (this.rootForms.value ?? []).filter((edge) =>
      permissions.find((perm) =>
        perm.forms.includes(edge.node.slug.replace(/-v\d/, ""))
      )
    );

    return raw
      .filter((edge) => edge.node.isPublished)
      .map((edge) => ({
        name: edge.node.name,
        value: [edge.node.slug, ...getRecursiveSources(edge.node, raw)],
        category: edge.node.meta.category || "others",
        order: edge.node.meta.order,
        isEqual(other) {
          return this.value.join(",") === other.value.join(",");
        },
      }));
  }

  @cached
  get serializedFilter() {
    return [
      ...(this._types
        ? [{ documentForms: this._types.split(",") }]
        : [{ documentForms: this.allForms }]),
      {
        metaValue: [
          { key: "camac-instance-id", value: this._instanceId },
          { key: answerSlugs.specialId, value: this._specialId },
          {
            key: "submit-date",
            value: DateTime.fromISO(this._submitFrom).startOf("day").toISO(),
            lookup: "GTE",
          },
          {
            key: "submit-date",
            value: DateTime.fromISO(this._submitTo).endOf("day").toISO(),
            lookup: "LTE",
          },
        ].filter(({ value }) => !isEmpty(value)),
      },
      {
        searchAnswers: [
          {
            questions: [
              answerSlugs.objectStreet,
              answerSlugs.objectNumber,
              answerSlugs.objectZIP,
              answerSlugs.objectLocation,
            ],
            value: this._address,
          },
          {
            questions: [
              answerSlugs.firstNameApplicant,
              answerSlugs.lastNameApplicant,
              answerSlugs.juristicNameApplicant,
            ],
            value: this._applicant,
          },
        ].filter(({ value }) => !isEmpty(value)),
      },
      {
        hasAnswer: [
          {
            question: answerSlugs.parcelNumber,
            lookup: "CONTAINS",
            value: this._parcel,
          },
        ].filter(({ value }) => !isEmpty(value)),
      },
    ];
  }

  @cached
  get serializedOrder() {
    const [key, direction] = this.order.split(":");
    return [
      {
        meta: key,
        direction: direction.toUpperCase(),
      },
    ];
  }

  @cached
  get serializedHeaders() {
    const camacFilters = {
      is_paper: (this._onlyPaper && this.session.isInternal) || null,
      instance_state: config.APPLICATION.instanceStateCategories[this.category],
      ...(this.session.group
        ? {}
        : {
            is_applicant: true,
          }),
    };

    return {
      "x-camac-filters": Object.entries(camacFilters)
        .filter(([, value]) => value)
        .map((entry) => entry.join("="))
        .join("&"),
    };
  }

  @dropTask
  *fetchRootForms() {
    return yield this.apollo.watchQuery(
      { query: getRootFormsQuery },
      "allForms.edges"
    );
  }

  async processNew(cases) {
    const instanceIds = cases.map(({ meta }) => meta["camac-instance-id"]);

    if (instanceIds.length) {
      await this.store.query("instance", {
        instance_id: instanceIds.join(","),
      });
    }

    return cases;
  }

  @action
  applyFilters(event) {
    event.preventDefault();

    this._applyFilters();
  }

  @action
  resetFilters(event) {
    event.preventDefault();

    this._resetFilters();
  }

  @action
  updateFilter(event) {
    this[event.target.name] = event.target.value;
  }

  @action
  updateOrder({ target: { value } }) {
    this.order = value;
  }
}
