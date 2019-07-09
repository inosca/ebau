import EmberObject, { computed } from "@ember/object";
import { reads } from "@ember/object/computed";
import moment from "moment";

export default EmberObject.extend({
  findAnswer(slug) {
    const answer =
      this.raw.document.answers.edges
        .map(({ node }) => node)
        .find(answer => answer.question.slug === slug) || {};

    const key = Object.keys(answer).find(key => /Value$/.test(key));

    return answer && key ? answer[key] : null;
  },

  id: reads("raw.meta.camac-instance-id"),
  ebau: reads("raw.meta.ebau-number"),
  type: reads("raw.document.form.name"),
  municipality: computed(
    "municipalities.[]",
    "raw.document.answers.edges.[]",
    function() {
      const slug = this.findAnswer("gemeinde");
      const node = this.municipalities.find(m => m.slug === slug);

      return node && node.label;
    }
  ),
  address: computed("raw.document.answers.edges.[]", function() {
    return [
      [
        this.findAnswer("strasse-gesuchstellerin") ||
          this.findAnswer("strasse-flurname"),
        this.findAnswer("nummer-gesuchstellerin") || this.findAnswer("nr")
      ]
        .filter(Boolean)
        .join(" ")
        .trim(),
      [
        this.findAnswer("plz-gesuchstellerin") || null,
        this.findAnswer("ort-gesuchstellerin") ||
          this.findAnswer("ort-grundstueck")
      ]
        .filter(Boolean)
        .join(" ")
        .trim()
    ]
      .filter(Boolean)
      .join(", ")
      .trim();
  }),
  submitDate: computed("raw.meta.submit-date", function() {
    const raw = this.get("raw.meta.submit-date");

    return raw ? moment(raw) : null;
  }),
  status: reads("instance.attributes.public-status"),
  description: computed("raw.document.answers.edges.[]", function() {
    return (
      this.findAnswer("anfrage-zur-vorabklaerung") ||
      this.findAnswer("beschreibung-bauvorhaben")
    );
  })
});
