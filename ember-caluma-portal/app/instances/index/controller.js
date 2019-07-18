import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";
import QueryParams from "ember-parachute";
import Document from "ember-caluma-portal/lib/document";
import { getOwner } from "@ember/application";
import { reads } from "@ember/object/computed";
import moment from "moment";
import { isEmpty } from "@ember/utils";
import formDataEntries from "form-data-entries";

import getDocumentsQuery from "ember-caluma-portal/gql/queries/get-documents";
import getMunicipalitiesQuery from "ember-caluma-portal/gql/queries/get-municipalities";
import getRootFormsQuery from "ember-caluma-portal/gql/queries/get-root-forms";

const getHasAnswerFilters = ({ parcel: value }) =>
  [
    {
      question: "parzellennummer",
      lookup: "CONTAINS",
      value
    }
  ].filter(({ value }) => !isEmpty(value));

const getMetaValueFilters = ({ instanceId, ebau, submitFrom, submitTo }) =>
  [
    { key: "camac-instance-id", value: instanceId },
    { key: "ebau-number", value: ebau },
    { key: "submit-date", value: submitFrom, lookup: "GTE" },
    { key: "submit-date", value: submitTo, lookup: "LTE" }
  ].filter(({ value }) => !isEmpty(value));

const DATE_URL_FORMAT = "YYYY-MM-DD";
const DATE_FORMAT = "DD.MM.YYYY";

const dateQueryParam = {
  serialize(value) {
    const date = moment(value, DATE_FORMAT);

    return date.isValid() ? date.format(DATE_URL_FORMAT) : this.defaultValue;
  },
  deserialize(value) {
    const date = moment(value, DATE_URL_FORMAT);

    return date.isValid() ? date.format(DATE_URL_FORMAT) : this.defaultValue;
  }
};

const queryParams = new QueryParams({
  type: {
    defaultValue: "",
    refresh: true
  },
  instanceId: {
    defaultValue: "",
    refresh: true,
    serialize(value) {
      const int = parseInt(value);

      return !isNaN(int) ? int : this.defaultValue;
    },
    deserialize(value) {
      const int = parseInt(value);

      return !isNaN(int) ? int : this.defaultValue;
    }
  },
  ebau: {
    defaultValue: "",
    refresh: true
  },
  parcel: {
    defaultValue: "",
    refresh: true
  },
  submitFrom: {
    defaultValue: "",
    refresh: true,
    ...dateQueryParam
  },
  submitTo: {
    defaultValue: "",
    refresh: true,
    ...dateQueryParam
  }
});

export default Controller.extend(queryParams.Mixin, {
  apollo: service(),
  fetch: service(),

  setup() {
    this.getMunicipalities.perform();
    this.getRootForms.perform();

    this.set("documents", []);
    this.fetchData.perform();
  },

  queryParamsDidChange({ shouldRefresh }) {
    if (shouldRefresh) {
      this.set("documents", []);
      this.fetchData.perform();
    }
  },

  reset(_, isExiting) {
    if (isExiting) {
      this.fetchData.cancelAll({ resetState: true });
      this.getInstances.cancelAll({ resetState: true });

      this.resetQueryParams();
    }
  },

  getRootForms: task(function*() {
    return (yield this.apollo.query(
      { query: getRootFormsQuery },
      "allForms.edges"
    )).map(({ node }) => node);
  }),

  getMunicipalities: task(function*() {
    return (yield this.apollo.query(
      { query: getMunicipalitiesQuery },
      "allQuestions.edges.firstObject.node.options.edges"
    )).map(({ node }) => node);
  }),

  getInstances: task(function*(ids) {
    if (isEmpty(ids)) return [];

    const response = yield this.fetch.fetch(
      `/api/v1/instances?ids=${ids.join(",")}`
    );

    const { data } = yield response.json();

    return data;
  }),

  pageInfo: reads("fetchData.lastSuccessful.value.pageInfo"),
  fetchData: task(function*(cursor = null) {
    try {
      const forms = yield this.getRootForms.last;

      const raw = yield this.apollo.query(
        {
          query: getDocumentsQuery,
          variables: {
            cursor,
            form: this.type,
            forms: forms.map(({ slug }) => slug),
            metaValueFilters: getMetaValueFilters(this.allQueryParams),
            hasAnswerFilters: getHasAnswerFilters(this.allQueryParams)
          }
        },
        "allDocuments"
      );
      const rawDocuments = raw.edges.map(({ node }) => node);

      const municipalities = yield this.getMunicipalities.last;
      const instances = yield this.getInstances.perform(
        rawDocuments.map(({ meta }) => meta["camac-instance-id"])
      );

      const documents = rawDocuments.map(raw => {
        return Document.create(getOwner(this).ownerInjection(), {
          raw,
          instance: instances.find(
            ({ id }) => parseInt(id) === parseInt(raw.meta["camac-instance-id"])
          ),
          municipalities
        });
      });

      this.set("documents", [...this.documents, ...documents]);

      Object.assign(raw.pageInfo, { totalCount: raw.totalCount });

      return raw;
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
    }
  }).restartable(),

  applyFilters: task(function*(e) {
    e.preventDefault();

    const data = formDataEntries(e.srcElement).reduce(
      (obj, [k, v]) => ({ ...obj, [k]: v }),
      {}
    );

    yield this.setProperties(data);
  }).drop(),

  resetFilters: task(function*() {
    yield this.resetQueryParams();
  })
});
