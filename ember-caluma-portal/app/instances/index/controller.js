import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";
import QueryParams from "ember-parachute";
import Document from "ember-caluma-portal/lib/document";
import { getOwner } from "@ember/application";
import { computed } from "@ember/object";
import { reads } from "@ember/object/computed";
import moment from "moment";
import { isEmpty } from "@ember/utils";
import formDataEntries from "form-data-entries";
import { ObjectQueryManager } from "ember-apollo-client";

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
        "ort-gesuchstellerin"
      ],
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
  address: {
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
  },
  order: {
    defaultValue: "META_CAMAC_INSTANCE_ID_DESC",
    refresh: true
  }
});

export default Controller.extend(queryParams.Mixin, ObjectQueryManager, {
  fetch: service(),

  orderOptions: computed(function() {
    return [
      {
        value: "META_CAMAC_INSTANCE_ID_DESC",
        label: "instances.instanceId",
        direction: "instances.desc"
      },
      {
        value: "META_CAMAC_INSTANCE_ID_ASC",
        label: "instances.instanceId",
        direction: "instances.asc"
      },
      {
        value: "META_EBAU_NUMBER_DESC",
        label: "instances.ebau",
        direction: "instances.desc"
      },
      {
        value: "META_EBAU_NUMBER_ASC",
        label: "instances.ebau",
        direction: "instances.asc"
      },
      {
        value: "META_SUBMIT_DATE_DESC",
        label: "instances.submitDate",
        direction: "instances.desc"
      },
      {
        value: "META_SUBMIT_DATE_ASC",
        label: "instances.submitDate",
        direction: "instances.asc"
      }
    ];
  }),

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

  reset() {
    this.fetchData.cancelAll({ resetState: true });

    this.resetQueryParams();
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

  pageInfo: reads("fetchData.lastSuccessful.value.pageInfo"),
  fetchData: task(function*(cursor = null) {
    try {
      const forms = yield this.getRootForms.last;

      const raw = yield this.apollo.query(
        {
          query: getDocumentsQuery,
          variables: {
            cursor,
            order: this.order,
            form: this.type,
            forms: forms.map(({ slug }) => slug),
            metaValueFilters: getMetaValueFilters(this.allQueryParams),
            hasAnswerFilters: getHasAnswerFilters(this.allQueryParams),
            searchAnswersFilters: getSearchAnswersFilters(this.allQueryParams)
          },
          fetchPolicy: "network-only"
        },
        "allDocuments"
      );
      const rawDocuments = raw.edges.map(({ node }) => node);

      const municipalities = yield this.getMunicipalities.last;

      yield this.store.query("instance", {
        instance_id: rawDocuments.map(({ meta }) => meta["camac-instance-id"])
      });

      const documents = rawDocuments.map(raw => {
        return Document.create(getOwner(this).ownerInjection(), {
          raw,
          instance: this.store.peekRecord(
            "instance",
            raw.meta["camac-instance-id"]
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
