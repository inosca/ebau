import Controller, { inject as controller } from "@ember/controller";
import { reads } from "@ember/object/computed";
import { queryManager } from "ember-apollo-client";
import getOverviewDocumentsQuery from "ember-caluma-portal/gql/queries/get-overview-documents";
import { dropTask, lastValue } from "ember-concurrency-decorators";
import QueryParams from "ember-parachute";

const findAnswer = (answers, slug) => {
  const answer = answers.find(answer => answer.question.slug === slug);

  if (!answer) {
    return null;
  }

  const key = Object.keys(answer).find(key => /Value$/.test(key));

  return answer[key];
};

function getAddress(answers) {
  const street = findAnswer(answers, "strasse-flurname");
  const number = findAnswer(answers, "nr");
  const city = findAnswer(answers, "ort-grundstueck");
  return `${street} ${number}, ${city}`;
}

function getEbauNr(document) {
  return document.node.meta["ebau-number"];
}

function getType(document) {
  return document.node.form.name;
}

function getMunicipality(document) {
  const answer = document.node.answers.edges.find(
    answer => answer.node.question.slug === "gemeinde"
  );
  return (
    answer &&
    answer.node.question.options.edges.find(({ node: { slug } }) => {
      return answer.node.stringValue === slug;
    }).node.label
  );
}

function getBuildingSpecification(answers) {
  return findAnswer(answers, "beschreibung-bauvorhaben");
}

export default class InstancesEditIndexController extends Controller.extend(
  new QueryParams().Mixin
) {
  @queryManager apollo;

  @controller("instances.edit") editController;
  @reads("editController.feedbackTask.isRunning") feedbackLoading;
  @reads("editController.feedback") feedback;
  @reads("editController.instance.instanceState.name") instanceState;
  @reads("editController.instance.activeService.name") activeService;

  setup() {
    this.dataTask.perform(this.model);
  }

  @lastValue("dataTask") data;
  @dropTask
  *dataTask() {
    const allDocuments = yield this.apollo.query(
      {
        fetchPolicy: "network-only",
        query: getOverviewDocumentsQuery,
        variables: {
          instanceId: this.model
        }
      },
      "allDocuments.edges"
    );
    const document = allDocuments.find(
      doc => doc.node.form.meta["is-main-form"]
    );
    const answers = document.node.answers.edges.map(answer => answer.node);

    return {
      address: getAddress(answers),
      ebauNr: getEbauNr(document),
      type: getType(document),
      municipality: getMunicipality(document),
      buildingSpecification: getBuildingSpecification(answers)
    };
  }
}
