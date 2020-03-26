import Controller, { inject as controller } from "@ember/controller";
import { get } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import getOverviewDocumentsQuery from "ember-caluma-portal/gql/queries/get-overview-documents";
import { dropTask, lastValue } from "ember-concurrency-decorators";

const findAnswer = (answers, slug) => {
  const answer = answers.find(answer => answer.question.slug === slug);

  if (!answer) {
    return null;
  }

  const key = Object.keys(answer).find(key => /Value$/.test(key));

  return answer[key];
};

function getAddress(answers) {
  const street =
    findAnswer(answers, "strasse-flurname") ||
    findAnswer(answers, "strasse-gesuchstellerin");

  const number =
    findAnswer(answers, "nr") || findAnswer(answers, "nummer-gesuchstellerin");

  const city =
    findAnswer(answers, "ort-grundstueck") ||
    findAnswer(answers, "ort-gesuchstellerin");

  return [[street, number].filter(Boolean).join(" "), city]
    .filter(Boolean)
    .join(", ");
}

function getEbauNr(document) {
  return document.node.meta["ebau-number"];
}

function getType(document) {
  return document.node.form.name;
}

function getMunicipality(answers) {
  const answer = answers.find(answer => answer.question.slug === "gemeinde");
  const selectedOption =
    answer &&
    answer.question.options.edges.find(option => {
      return answer.stringValue === option.node.slug;
    });

  return selectedOption && selectedOption.node.label;
}

function getBuildingSpecification(answers) {
  return findAnswer(answers, "beschreibung-bauvorhaben");
}

export default class InstancesEditIndexController extends Controller {
  @queryManager apollo;
  @service fetch;

  @controller("instances.edit") editController;
  @reads("editController.feedbackTask.isRunning") feedbackLoading;
  @reads("editController.decisionTask.isRunning") decisionLoading;
  @reads("editController.feedback") feedback;
  @reads("editController.decision") decision;
  @reads("editController.instance") instance;

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
    const document = allDocuments.find(doc =>
      get(doc, "node.form.meta.is-main-form")
    );
    const answers = document.node.answers.edges.map(answer => answer.node);

    return {
      address: getAddress(answers),
      ebauNr: getEbauNr(document),
      type: getType(document),
      municipality: getMunicipality(answers),
      buildingSpecification: getBuildingSpecification(answers)
    };
  }

  @dropTask
  *createModification() {
    yield this.copy.perform(true);
  }

  @dropTask
  *createCopy() {
    yield this.copy.perform();
  }

  @dropTask
  *copy(isModification = false) {
    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify({
        data: {
          attributes: {
            "copy-source": this.model,
            "is-modification": isModification
          },
          type: "instances"
        }
      })
    });

    const { data } = yield response.json();

    yield this.transitionToRoute("instances.edit", data.id);
  }
}
