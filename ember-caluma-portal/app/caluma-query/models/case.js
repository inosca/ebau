import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import CaseModel from "ember-caluma/caluma-query/models/case";
import moment from "moment";

export default class CustomCaseModel extends CaseModel {
  @service store;

  _findAnswer(slug) {
    const answers = this.raw.document.answers.edges.map(({ node }) => node);
    const answer =
      answers.find((answer) => answer.question.slug === slug) || {};

    const key = Object.keys(answer).find((key) => /Value$/.test(key));

    return answer && key ? answer[key] : null;
  }

  @reads("raw.meta.camac-instance-id") instanceId;
  @reads("raw.meta.ebau-number") ebau;
  @reads("raw.document.form.name") type;
  @reads("instance.status") status;
  @reads("instance.isPaper") isPaper;
  @reads("instance.isModification") isModification;

  get instance() {
    return this.store.peekRecord("instance", this.instanceId);
  }

  get municipality() {
    const slug = this._findAnswer("gemeinde");

    return (
      slug &&
      this.store
        .peekRecord("public-service", slug)
        ?.name?.replace(/Leitbehörde|Municipalité/, "")
        .trim()
    );
  }

  get submitDate() {
    const raw = this.raw.meta["submit-date"];

    return raw ? moment(raw) : null;
  }

  get description() {
    return this._findAnswer("beschreibung-bauvorhaben");
  }

  get address() {
    return [
      [
        this._findAnswer("strasse-gesuchstellerin") ||
          this._findAnswer("strasse-flurname"),
        this._findAnswer("nummer-gesuchstellerin") || this._findAnswer("nr"),
      ]
        .filter(Boolean)
        .join(" ")
        .trim(),
      [
        this._findAnswer("plz-gesuchstellerin") || null,
        this._findAnswer("ort-gesuchstellerin") ||
          this._findAnswer("ort-grundstueck"),
      ]
        .filter(Boolean)
        .join(" ")
        .trim(),
    ]
      .filter(Boolean)
      .join(", ")
      .trim();
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
        questions: [
          "gemeinde"
          "strasse-gesuchstellerin"
          "nummer-gesuchstellerin"
          "plz-gesuchstellerin"
          "ort-gesuchstellerin"
          "beschreibung-bauvorhaben"
          "gemeinde"
          "strasse-flurname"
          "nr"
          "ort-grundstueck"
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
