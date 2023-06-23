import Component from "@glimmer/component";
import { DateTime } from "luxon";

export default class CalculatedPublicationDateComponent extends Component {
  get calculatedPublicationDate() {
    const initialDate = this.args.field.document.findField(
      this.args.field.raw.question.meta.initialPublicationDateSlug,
    );

    if (!initialDate.answer.value) {
      return "";
    }

    return DateTime.fromISO(initialDate.answer.value)
      .plus({ days: this.args.field.raw.question.meta.publicationDuration })
      .toFormat("dd.MM.yyyy");
  }
}
