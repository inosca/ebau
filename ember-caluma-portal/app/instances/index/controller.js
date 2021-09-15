import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency-decorators";
import moment from "moment";

import { Mixin } from "./query-params";

import config from "caluma-portal/config/environment";
import getRootFormsQuery from "caluma-portal/gql/queries/get-root-forms.graphql";

const { answerSlugs } = config.APPLICATION;

const getRecursiveSources = (form, forms) => {
  if (!form.source?.slug) {
    return [];
  }

  const source = forms.find(({ slug }) => slug === form.source.slug);

  return [source.slug, ...getRecursiveSources(source, forms)];
};

const toDateTime = (date) => (date.isValid() ? date.utc().format() : null);

export default class InstancesIndexController extends Controller.extend(Mixin) {
  @queryManager apollo;

  @service intl;
  @service session;

  @calumaQuery({ query: allCases, options: "options" }) cases;

  get options() {
    return {
      pageSize: 15,
      processNew: (cases) => this.processNew(cases),
    };
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

  setup() {
    this.getRootForms.perform();
    this.getCases.perform();
  }

  reset() {
    this.resetQueryParams();

    this.getRootForms.cancelAll({ reset: true });
    this.getCases.cancelAll({ reset: true });
  }

  get allForms() {
    return (this.getRootForms.lastSuccessful?.value || []).map(
      (form) => form.slug
    );
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
    const raw = (this.getRootForms.lastSuccessful?.value || []).filter(
      (form) =>
        this.isInternal || !config.ebau.internalForms.includes(form.slug)
    );

    return raw
      .filter((form) => form.isPublished)
      .map((form) => ({
        name: form.name,
        value: [form.slug, ...getRecursiveSources(form, raw)],
        category: form.meta.category || "others",
        order: form.meta.order,
        isEqual(other) {
          return this.value.join(",") === other.value.join(",");
        },
      }));
  }

  get selectedTypes() {
    return this.forms.filter((form) =>
      form.value.some((value) => this.types.includes(value))
    );
  }

  set selectedTypes(value) {
    this.set(
      "types",
      value.flatMap((form) => form.value)
    );
  }

  get serializedFilter() {
    return [
      ...(this.types.length
        ? [{ documentForms: this.types }]
        : [{ documentForms: this.allForms }]),
      {
        metaValue: [
          { key: "camac-instance-id", value: this.instanceId },
          { key: answerSlugs.specialId, value: this.specialId },
          {
            key: "submit-date",
            value: toDateTime(moment(this.submitFrom).startOf("day")),
            lookup: "GTE",
          },
          {
            key: "submit-date",
            value: toDateTime(moment(this.submitTo).endOf("day")),
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
            value: this.address,
          },
        ].filter(({ value }) => !isEmpty(value)),
      },
      {
        hasAnswer: [
          {
            question: answerSlugs.parcelNumber,
            lookup: "CONTAINS",
            value: this.parcel,
          },
        ].filter(({ value }) => !isEmpty(value)),
      },
    ];
  }

  get serializedOrder() {
    const [key, direction] = this.order.split(":");
    return [
      {
        meta: key,
        direction: direction.toUpperCase(),
      },
    ];
  }

  get serializedHeaders() {
    const camacFilters = this.session.group ? {} : { is_applicant: true };

    return {
      "x-camac-filters": Object.entries(camacFilters)
        .filter(([, value]) => value)
        .map((entry) => entry.join("="))
        .join("&"),
    };
  }

  @dropTask
  *getRootForms() {
    return (yield this.apollo.query(
      { query: getRootFormsQuery },
      "allForms.edges"
    )).map(({ node }) => node);
  }

  @dropTask
  *getCases() {
    yield this.getRootForms.last;

    yield this.cases.fetch({
      order: this.serializedOrder,
      filter: this.serializedFilter,
      queryOptions: {
        context: {
          headers: this.serializedHeaders,
        },
      },
    });
  }

  @dropTask
  *getMoreCases() {
    yield this.cases.fetchMore();
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

  @dropTask
  *applyFilters(event) {
    event.preventDefault();

    yield this.getCases.perform();
  }

  @dropTask
  *resetFilters(event) {
    event.preventDefault();

    yield this.resetQueryParams();
    yield this.getCases.perform();
  }

  @action
  updateFilter(event) {
    this.set(event.target.name, event.target.value);
  }

  @action
  updateDate(prop, value) {
    this.set(prop, moment(value));
  }

  @action
  updateOrder({ target: { value } }) {
    this.set("order", value);
    this.getCases.perform();
  }
}
