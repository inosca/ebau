import EmberObject, { computed } from "@ember/object";
import { reads } from "@ember/object/computed";
import moment from "moment";

export default class Case extends EmberObject {
  findAnswer(slug) {
    const answer =
      this.answers.find((answer) => answer.question.slug === slug) || {};

    const key = Object.keys(answer).find((key) => /Value$/.test(key));

    return answer && key ? answer[key] : null;
  }

  @computed("raw.document.answers.edges.[]")
  get answers() {
    return this.raw.document.answers.edges.map(({ node }) => node);
  }

  @reads("raw.meta.camac-instance-id") instanceId;
  @reads("raw.meta.ebau-number") ebau;

  @reads("raw.document.form.name") type;

  @reads("instance.status") status;
  @reads("instance.isPaper") isPaper;
  @reads("instance.isModification") isModification;

  @computed("municipalities.[]", "answers.[]")
  get municipality() {
    const slug = this.findAnswer("gemeinde");
    const node = this.municipalities.find((m) => m.slug === slug);

    return node && node.label;
  }

  @computed("answers.[]")
  get address() {
    return [
      [
        this.findAnswer("strasse-gesuchstellerin") ||
          this.findAnswer("strasse-flurname"),
        this.findAnswer("nummer-gesuchstellerin") || this.findAnswer("nr"),
      ]
        .filter(Boolean)
        .join(" ")
        .trim(),
      [
        this.findAnswer("plz-gesuchstellerin") || null,
        this.findAnswer("ort-gesuchstellerin") ||
          this.findAnswer("ort-grundstueck"),
      ]
        .filter(Boolean)
        .join(" ")
        .trim(),
    ]
      .filter(Boolean)
      .join(", ")
      .trim();
  }

  @computed("raw.meta.submit-date")
  get submitDate() {
    const raw = this.get("raw.meta.submit-date");

    return raw ? moment(raw) : null;
  }

  @computed("answers.[]")
  get description() {
    return (
      this.findAnswer("anfrage-zur-vorabklaerung") ||
      this.findAnswer("beschreibung-bauvorhaben")
    );
  }
}
