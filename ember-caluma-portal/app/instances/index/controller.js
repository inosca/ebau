import { getOwner } from "@ember/application";
import Controller from "@ember/controller";
import { computed, set, action } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import { queryManager } from "ember-apollo-client";
import getDocumentsQuery from "ember-caluma-portal/gql/queries/get-documents";
import getMunicipalitiesQuery from "ember-caluma-portal/gql/queries/get-municipalities";
import getRootFormsQuery from "ember-caluma-portal/gql/queries/get-root-forms";
import Document from "ember-caluma-portal/lib/document";
import {
  restartableTask,
  dropTask,
  lastValue
} from "ember-concurrency-decorators";
import QueryParams from "ember-parachute";
import moment from "moment";

const MODIFICATION_FORMS = [
  "baugesuch",
  "baugesuch-generell",
  "baugesuch-mit-uvp"
];

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
    defaultValue: null,
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
    defaultValue: null,
    replace: true,
    ...dateQueryParam
  },
  submitTo: {
    defaultValue: null,
    replace: true,
    ...dateQueryParam
  },
  order: {
    defaultValue: "META_CAMAC_INSTANCE_ID_DESC",
    replace: true
  },
  modify: {
    defaultValue: false,
    replace: true
  }
});

export default class InstancesIndexController extends Controller.extend(
  queryParams.Mixin
) {
  @service fetch;
  @queryManager apollo;

  get orderOptions() {
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
  }

  setup() {
    this.getMunicipalities.perform();
    this.getRootForms.perform();

    this.set("documents", []);
    this.fetchData.perform();
  }

  reset() {
    this.resetQueryParams();
    this.set("documents", []);

    this.getMunicipalities.cancelAll({ reset: true });
    this.getRootForms.cancelAll({ reset: true });
    this.fetchData.cancelAll({ reset: true });
  }

  @lastValue("getRootForms") _rootForms;
  @computed("_rootForms.[]", "modify")
  get rootForms() {
    return (this._rootForms || []).map(form => {
      return {
        ...form,
        disabled: this.modify ? !MODIFICATION_FORMS.includes(form.slug) : false
      };
    });
  }

  @computed("rootForms.@each.slug", "types.[]")
  get selectedTypes() {
    return this.rootForms.filter(form => this.types.includes(form.slug));
  }

  set selectedTypes(value) {
    this.set(
      "types",
      value.map(form => form.slug)
    );

    return value;
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
  }

  @dropTask
  *applyFilters(event) {
    event.preventDefault();

    this.set("documents", []);
    yield this.fetchData.perform();
  }

  @dropTask
  *resetFilters(event) {
    event.preventDefault();

    if (this.modify) {
      yield this.startModification.perform();
    } else {
      yield this.resetQueryParams();

      this.set("documents", []);
      yield this.fetchData.perform();
    }
  }

  @dropTask
  *startModification() {
    this.resetQueryParams();

    this.setProperties({
      modify: true,
      submitTo: moment.utc().toDate(),
      types: [...MODIFICATION_FORMS],
      documents: []
    });

    yield this.fetchData.perform();
  }

  @dropTask
  *endModification() {
    this.resetQueryParams();

    this.setProperties({
      modify: false,
      documents: []
    });

    yield this.fetchData.perform();
  }

  @dropTask
  *createModification(instanceId) {
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
