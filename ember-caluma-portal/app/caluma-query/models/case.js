import { inject as service } from "@ember/service";
import CaseModel from "ember-caluma/caluma-query/models/case";
import moment from "moment";

import config from "caluma-portal/config/environment";

const { answerSlugs } = config.APPLICATION;

export default class CustomCaseModel extends CaseModel {
  @service store;

  _findAnswer(slug) {
    const answers = this.raw.document.answers.edges.map(({ node }) => node);
    const answer =
      answers.find((answer) => answer.question.slug === slug) || {};

    const key = Object.keys(answer).find((key) => /Value$/.test(key));

    return answer && key ? answer[key] : null;
  }

  get instanceId() {
    return this.raw.meta["camac-instance-id"];
  }

  get instance() {
    return this.store.peekRecord("instance", this.instanceId);
  }

  get specialId() {
    return this.raw.meta[answerSlugs.specialId];
  }

  get type() {
    return this.raw.document.form.name;
  }

  get status() {
    return this.instance.status;
  }

  get isPaper() {
    return this.instance.isPaper;
  }

  get isModification() {
    return this.instance.isModification;
  }

  get municipality() {
    const slug = this._findAnswer(answerSlugs.municipality);

    return (
      slug &&
      this.store
        .peekRecord(config.APPLICATION.municipalityModel, slug)
        ?.name?.replace(/Leitbehörde|Municipalité/, "")
        .trim()
    );
  }

  get submitDate() {
    const raw = this.raw.meta["submit-date"];

    return raw ? moment(raw) : null;
  }

  get description() {
    return this._findAnswer(answerSlugs.description);
  }

  get address() {
    const streetAndNr = [
      this._findAnswer(answerSlugs.objectStreet),
      this._findAnswer(answerSlugs.objectNumber),
    ]
      .filter(Boolean)
      .join(" ")
      .trim();
    const city = this._findAnswer(answerSlugs.objectLocation)?.trim();

    return [streetAndNr, city].filter(Boolean).join(", ").trim();
  }

  static fragment = `{
    id
    meta
    document {
      id
      form {
        slug
        name
      }
      answers(
        visibleInContext: true
        questions: [
          "${answerSlugs.municipality}"
          "${answerSlugs.description}"
          "${answerSlugs.objectStreet}"
          "${answerSlugs.objectNumber}"
          "${answerSlugs.objectLocation}"
        ]
      ) {
        edges {
          node {
            id
            question {
              slug
            }
            ...on StringAnswer {
              stringValue: value
            }
            ...on IntegerAnswer {
              integerValue: value
            }
          }
        }
      }
    }
  }`;
}
