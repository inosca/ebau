import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { useTask } from "ember-resources";
import moment from "moment";
import { TrackedObject } from "tracked-built-ins";
import { dedupeTracked, cached } from "tracked-toolbox";

import config from "caluma-portal/config/environment";
import getRootFormsQuery from "caluma-portal/gql/queries/get-root-forms.graphql";

const { answerSlugs } = config.APPLICATION;
const DATE_URL_FORMAT = "YYYY-MM-DD";

const getRecursiveSources = (form, forms) => {
  if (!form.source?.slug) {
    return [];
  }

  const source = forms.find((edge) => edge.node.slug === form.source.slug);

  return [source.node.slug, ...getRecursiveSources(source.node, forms)];
};

const toDateTime = (date) => (date.isValid() ? date.utc().format() : null);

const dateFilter = {
  serialize(value) {
    const date = moment.utc(value);

    return date.isValid() ? date.utc().format(DATE_URL_FORMAT) : null;
  },
  deserialize(value) {
    const date = moment.utc(value, DATE_URL_FORMAT);

    return date.isValid() ? date.toDate() : null;
  },
};

function trackedFilter({
  serialize = (value) => value,
  deserialize = (value) => value,
  defaultValue,
}) {
  return function decorator(target, property) {
    if (!Object.prototype.hasOwnProperty.call(target, "_filters")) {
      target._filters = new TrackedObject();
      target._applyFilters = function () {
        this._filtersConfig.forEach(({ privateKey, publicKey, serialize }) => {
          this[privateKey] = serialize.call(this, this[publicKey]);
        });
      };
      target._resetFilters = function () {
        this._filtersConfig.forEach(
          ({ publicKey, privateKey, defaultValue }) => {
            this._filters[publicKey] = defaultValue;
            this[privateKey] = defaultValue;
          }
        );
      };
    }

    const privateKey = `_${property}`;

    Object.defineProperty(
      target,
      privateKey,
      dedupeTracked(target, privateKey, { initializer: () => defaultValue })
    );

    target._filters[property] = defaultValue;
    target._filtersConfig = [
      ...(target._filtersConfig ?? []),
      { privateKey, publicKey: property, serialize, deserialize, defaultValue },
    ];

    return cached(target, property, {
      enumerable: true,
      configurable: false,
      get() {
        const filtersValue = this._filters[property];
        const targetValue = this[privateKey];

        const value =
          filtersValue === defaultValue && targetValue !== defaultValue
            ? targetValue
            : filtersValue;

        return deserialize.call(this, value);
      },
      set(value) {
        this._filters[property] = serialize.call(this, value);
      },
    });
  };
}

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

  @dedupeTracked order = "camac-instance-id:desc";
  @dedupeTracked category = config.APPLICATION.defaultInstanceStateCategory;

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
  @trackedFilter({ ...dateFilter, defaultValue: null }) submitFrom;
  @trackedFilter({ ...dateFilter, defaultValue: null }) submitTo;

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

  rootForms = useTask(this, this.fetchRootForms, () => {});

  get categories() {
    return Object.keys(config.APPLICATION.instanceStateCategories);
  }

  get orderOptions() {
    return [
      {
        value: "camac-instance-id:desc",
        label: `instances.instance-id-${config.APPLICATION.name}`,
        direction: "instances.desc",
      },
      {
        value: "camac-instance-id:asc",
        label: `instances.instance-id-${config.APPLICATION.name}`,
        direction: "instances.asc",
      },
      {
        value: `${answerSlugs.specialId}:desc`,
        label: `instances.special-id-${config.APPLICATION.name}`,
        direction: "instances.desc",
      },
      {
        value: `${answerSlugs.specialId}:asc`,
        label: `instances.special-id-${config.APPLICATION.name}`,
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
              groupName: this.intl.t(
                `instances.new.${category}.title-${config.APPLICATION.name}`
              ),
              options,
            }
          : null;
      })
      .filter(Boolean);
  }

  get forms() {
    const raw = (this.rootForms.value ?? []).filter(
      (edge) =>
        this.isInternal || !config.ebau.internalForms.includes(edge.node.slug)
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
            value: toDateTime(moment(this._submitFrom).startOf("day")),
            lookup: "GTE",
          },
          {
            key: "submit-date",
            value: toDateTime(moment(this._submitTo).endOf("day")),
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
              answerSlugs.objectLocation,
            ],
            value: this._address,
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
  updateDate(prop, value) {
    this[prop] = moment(value);
  }

  @action
  updateOrder({ target: { value } }) {
    this.order = value;
  }
}
