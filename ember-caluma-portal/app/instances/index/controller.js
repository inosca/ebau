import { getOwner } from "@ember/application";
import Controller from "@ember/controller";
import { computed, set, action } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import { queryManager } from "ember-apollo-client";
import {
  restartableTask,
  dropTask,
  lastValue,
} from "ember-concurrency-decorators";
import QueryParams from "ember-parachute";
import moment from "moment";

import config from "ember-caluma-portal/config/environment";
import getCasesQuery from "ember-caluma-portal/gql/queries/get-cases";
import getMunicipalitiesQuery from "ember-caluma-portal/gql/queries/get-municipalities";
import getRootFormsQuery from "ember-caluma-portal/gql/queries/get-root-forms";
import Case from "ember-caluma-portal/lib/case";

const getOrder = (order) => [
  {
    meta: order.split(":")[0],
    direction: order.split(":")[1].toUpperCase(),
  },
];

const getHasAnswerFilters = ({ parcel: value }) =>
  [
    {
      question: "parzellennummer",
      lookup: "CONTAINS",
      value,
    },
  ].filter(({ value }) => !isEmpty(value));

const getSearchAnswersFilters = ({ address: value }) =>
  [
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
      value,
    },
  ].filter(({ value }) => !isEmpty(value));

const getMetaValueFilters = ({ instanceId, ebau, submitFrom, submitTo }) =>
  [
    { key: "camac-instance-id", value: instanceId },
    { key: "ebau-number", value: ebau },
    {
      key: "submit-date",
      value: toDateTime(moment(submitFrom).startOf("day")),
      lookup: "GTE",
    },
    {
      key: "submit-date",
      value: toDateTime(moment(submitTo).endOf("day")),
      lookup: "LTE",
    },
  ].filter(({ value }) => !isEmpty(value));

const DATE_URL_FORMAT = "YYYY-MM-DD";

const toDateTime = (date) => (date.isValid() ? date.utc().format() : null);

const dateQueryParam = {
  serialize(value) {
    const date = moment.utc(value);

    return date.isValid()
      ? date.utc().format(DATE_URL_FORMAT)
      : this.defaultValue;
  },
  deserialize(value) {
    const date = moment.utc(value, DATE_URL_FORMAT);

    return date.isValid() ? date.toDate() : this.defaultValue;
  },
};

const queryParams = new QueryParams({
  types: {
    defaultValue: [],
    replace: true,
    serialize(value) {
      return value.toString();
    },
    deserialize(value) {
      if (!value) {
        return [];
      }
      return value.split(",");
    },
  },
  instanceId: {
    defaultValue: null,
    replace: true,
    serialize(value) {
      const int = parseInt(value);

      return !isNaN(int) ? int : this.defaultValue;
    },
    deserialize(value) {
      const int = parseInt(value);

      return !isNaN(int) ? int : this.defaultValue;
    },
  },
  ebau: {
    defaultValue: "",
    replace: true,
  },
  parcel: {
    defaultValue: "",
    replace: true,
  },
  address: {
    defaultValue: "",
    replace: true,
  },
  submitFrom: {
    defaultValue: null,
    replace: true,
    ...dateQueryParam,
  },
  submitTo: {
    defaultValue: null,
    replace: true,
    ...dateQueryParam,
  },
  order: {
    defaultValue: "camac-instance-id:desc",
    replace: true,
  },
});

export default class InstancesIndexController extends Controller.extend(
  queryParams.Mixin
) {
  @service fetch;
  @service session;

  @queryManager apollo;

  get orderOptions() {
    return [
      {
        value: "camac-instance-id:desc",
        label: "instances.instanceId",
        direction: "instances.desc",
      },
      {
        value: "camac-instance-id:asc",
        label: "instances.instanceId",
        direction: "instances.asc",
      },
      {
        value: "ebau-number:desc",
        label: "instances.ebau",
        direction: "instances.desc",
      },
      {
        value: "ebau-number:asc",
        label: "instances.ebau",
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
    this.getMunicipalities.perform();
    this.getRootForms.perform();

    this.set("cases", []);
    this.fetchData.perform();
  }

  reset() {
    this.resetQueryParams();
    this.set("cases", []);

    this.getMunicipalities.cancelAll({ reset: true });
    this.getRootForms.cancelAll({ reset: true });
    this.fetchData.cancelAll({ reset: true });
  }

  @lastValue("getRootForms") rootForms;

  get formFilterOptions() {
    return (this.rootForms || [])
      .filter(
        (form) =>
          this.isInternal || !config.ebau.internalForms.includes(form.slug)
      )
      .filter(
        (form) =>
          config.ebau.enableRstaForms ||
          !config.ebau.rstaForms.includes(form.slug)
      );
  }

  @computed("rootForms.@each.slug", "types.[]")
  get selectedTypes() {
    return (this.rootForms || []).filter((form) =>
      this.types.includes(form.slug)
    );
  }

  set selectedTypes(value) {
    this.set(
      "types",
      value.map((form) => form.slug)
    );
  }

  @dropTask
  *getRootForms() {
    return (yield this.apollo.query(
      { query: getRootFormsQuery },
      "allForms.edges"
    )).map(({ node }) => node);
  }

  @dropTask
  *getMunicipalities() {
    return (yield this.apollo.query(
      { query: getMunicipalitiesQuery },
      "allQuestions.edges.firstObject.node.options.edges"
    )).map(({ node }) => node);
  }

  @reads("fetchData.lastSuccessful.value.pageInfo") pageInfo;

  @restartableTask
  *fetchData(cursor = null) {
    try {
      const forms = yield this.getRootForms.last;

      const raw = yield this.apollo.query(
        {
          query: getCasesQuery,
          variables: {
            cursor,
            order: getOrder(this.order),
            forms: this.types.length
              ? this.types
              : forms.map(({ slug }) => slug),
            metaValueFilters: getMetaValueFilters(this.allQueryParams),
            hasAnswerFilters: getHasAnswerFilters(this.allQueryParams),
            searchAnswersFilters: getSearchAnswersFilters(this.allQueryParams),
          },
          fetchPolicy: "network-only",
        },
        "allCases"
      );
      const rawCases = raw.edges.map(({ node }) => node);

      if (rawCases.length) {
        const municipalities = yield this.getMunicipalities.last;

        yield this.store.query("instance", {
          instance_id: rawCases
            .map(({ meta }) => meta["camac-instance-id"])
            .join(","),
        });

        const cases = rawCases.map((raw) => {
          return Case.create(getOwner(this).ownerInjection(), {
            raw,
            instance: this.store.peekRecord(
              "instance",
              raw.meta["camac-instance-id"]
            ),
            municipalities,
          });
        });

        this.set("cases", [...this.cases, ...cases]);
      }

      set(raw, "pageInfo", { ...raw.pageInfo, totalCount: raw.totalCount });

      return raw;
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
    }
  }

  @dropTask
  *applyFilters(event) {
    event.preventDefault();

    this.set("cases", []);
    yield this.fetchData.perform();
  }

  @dropTask
  *resetFilters(event) {
    event.preventDefault();

    yield this.resetQueryParams();

    this.set("cases", []);
    yield this.fetchData.perform();
  }

  @action
  updateFilter(event) {
    this.set(event.target.name, event.target.value);
  }

  @action
  updateDate(prop, value) {
    this.set(prop, moment(value));
  }
}
