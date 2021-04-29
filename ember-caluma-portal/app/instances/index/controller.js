import Controller from "@ember/controller";
import { action } from "@ember/object";
import { isEmpty } from "@ember/utils";
import { queryManager } from "ember-apollo-client";
import calumaQuery from "ember-caluma/caluma-query";
import { allCases } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";
import moment from "moment";

import { Mixin } from "./query-params";

import config from "caluma-portal/config/environment";
import getRootFormsQuery from "caluma-portal/gql/queries/get-root-forms.graphql";

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
        value: "ebau-number:desc",
        label: `instances.special-id-${config.APPLICATION.name}`,
        direction: "instances.desc",
      },
      {
        value: "ebau-number:asc",
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
    const raw = (this.getRootForms.lastSuccessful?.value || []).filter(
      (form) =>
        this.isInternal || !config.ebau.internalForms.includes(form.slug)
    );

    return raw
      .filter((form) => form.isPublished)
      .map((form) => ({
        name: form.name,
        value: [form.slug, ...getRecursiveSources(form, raw)],
        isEqual(other) {
          return this.value.join(",") === other.value.join(",");
        },
      }));
  }

  get selectedTypes() {
    return this.formFilterOptions.filter((form) =>
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
          { key: "ebau-number", value: this.ebau },
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
              "strasse-flurname",
              "strasse-gesuchstellerin",
              "nr",
              "nummer-gesuchstellerin",
              "plz-gesuchstellerin",
              "ort-grundstueck",
              "ort-gesuchstellerin",
            ],
            value: this.address,
          },
        ].filter(({ value }) => !isEmpty(value)),
      },
      {
        hasAnswer: [
          {
            question: "parzellennummer",
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
    });
  }

  @dropTask
  *getMoreCases() {
    yield this.cases.fetchMore();
  }

  async processNew(cases) {
    const instanceIds = cases
      .map(({ meta }) => meta["camac-instance-id"])
      .filter(Boolean);

    const serviceIds = cases
      .map(
        ({ document }) =>
          document.answers.edges
            .map(({ node }) => node)
            .find((answer) => answer.question.slug === "gemeinde")?.stringValue
      )
      .filter(Boolean);

    if (instanceIds.length) {
      await this.store.query("instance", {
        instance_id: instanceIds.join(","),
      });
    }

    if (serviceIds.length) {
      await this.store.query("public-service", {
        service_id: serviceIds.join(","),
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
