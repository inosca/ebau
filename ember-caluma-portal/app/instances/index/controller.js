import { getOwner } from "@ember/application";
import Controller from "@ember/controller";
import { computed, set } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import { queryManager } from "ember-apollo-client";
import getDocumentsQuery from "ember-caluma-portal/gql/queries/get-documents";
import getMunicipalitiesQuery from "ember-caluma-portal/gql/queries/get-municipalities";
import getRootFormsQuery from "ember-caluma-portal/gql/queries/get-root-forms";
import Document from "ember-caluma-portal/lib/document";
import { task } from "ember-concurrency";
import QueryParams from "ember-parachute";
import moment from "moment";

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
    {
      key: "submit-date",
      value: toDateTime(moment(submitFrom).startOf("day")),
      lookup: "GTE"
    },
    {
      key: "submit-date",
      value: toDateTime(moment(submitTo).endOf("day")),
      lookup: "LTE"
    }
  ].filter(({ value }) => !isEmpty(value));

const DATE_URL_FORMAT = "YYYY-MM-DD";

const toDateTime = date => (date.isValid() ? date.utc().format() : null);

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
  }
};

const queryParams = new QueryParams({
  types: {
    defaultValue: [],
    replace: true,
    serialize(value) {
      return value.toString();
    },
    deserialize(value) {
      return value.split(",");
    }
  },
  instanceId: {
    defaultValue: "",
    replace: true,
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
    replace: true
  },
  parcel: {
    defaultValue: "",
    replace: true
  },
  address: {
    defaultValue: "",
    replace: true
  },
  submitFrom: {
    defaultValue: "",
    replace: true,
    ...dateQueryParam
  },
  submitTo: {
    defaultValue: "",
    replace: true,
    ...dateQueryParam
  },
  order: {
    defaultValue: "META_CAMAC_INSTANCE_ID_DESC",
    replace: true
  },
  isModifification: {
    defaultValue: false,
    replace: true
  }
});

export default Controller.extend(queryParams.Mixin, {
  fetch: service(),

  apollo: queryManager(),

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

  getRootForms: task(function*() {
    return (yield this.apollo.query(
      { query: getRootFormsQuery },
      "allForms.edges"
    )).map(({ node }) => node);
  }),

  rootForms: reads("getRootForms.lastSuccessful.value"),
  selectedTypes: computed("rootForms", "types", {
    get() {
      return (this.rootForms || []).filter(form =>
        this.types.includes(form.slug)
      );
    },
    set(key, value) {
      this.set(
        "types",
        value.map(form => form.slug)
      );
      return value;
    }
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
            forms: this.types.length
              ? this.types
              : forms.map(({ slug }) => slug),
            metaValueFilters: getMetaValueFilters(this.allQueryParams),
            hasAnswerFilters: getHasAnswerFilters(this.allQueryParams),
            searchAnswersFilters: getSearchAnswersFilters(this.allQueryParams)
          },
          fetchPolicy: "network-only"
        },
        "allDocuments"
      );
      const rawDocuments = raw.edges.map(({ node }) => node);

      if (rawDocuments.length) {
        const municipalities = yield this.getMunicipalities.last;

        yield this.store.query("instance", {
          instance_id: rawDocuments
            .map(({ meta }) => meta["camac-instance-id"])
            .join(",")
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
      }

      set(raw, "pageInfo", { ...raw.pageInfo, totalCount: raw.totalCount });

      return raw;
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
    }
  }).restartable(),

  applyFilters: task(function*(e) {
    e.preventDefault();

    this.set("documents", []);
    yield this.fetchData.perform();
  }).drop(),

  resetFilters: task(function*() {
    yield this.resetQueryParams();
    this.set("documents", []);
    yield this.fetchData.perform();
  }),

  toggleModification: task(function*() {
    this.set("isModifification", !this.isModifification);
    this.set("submitTo", this.isModifification ? moment.utc().toDate() : null);
    this.set(
      "types",
      this.isModifification
        ? ["baugesuch", "baugesuch-generell", "baugesuch-mit-uvp"]
        : []
    );

    this.set("documents", []);
    yield this.fetchData.perform();
  }),

  createModification: task(function*(instanceId) {
    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify({
        data: {
          attributes: { "copy-source": instanceId },
          type: "instances",
          relationships: {
            form: {
              data: { id: 1, type: "forms" }
            }
          }
        }
      })
    });

    const {
      data: { id: newInstanceId }
    } = yield response.json();

    yield this.transitionToRoute("instances.edit", newInstanceId);
  }),

  actions: {
    updateDate(prop, value) {
      this.set(prop, moment(value));
    },
    updateFilter(e) {
      this.set(e.target.name, e.target.value);
    }
  }
});
