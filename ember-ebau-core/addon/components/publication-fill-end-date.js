import Component from "@glimmer/component";
import { task } from "ember-concurrency";
import { DateTime } from "luxon";

export default class PublicationFillEndDate extends Component {
  get #config() {
    return this.args.field.raw.question.meta["fill-end-date"] ?? {};
  }

  get minDate() {
    if (
      this.#config.minDateFromNow &&
      typeof this.#config.minDateFromNow === "number"
    ) {
      return new Date().fp_incr(this.#config.minDateFromNow);
    }
    return undefined;
  }

  get maxDate() {
    if (
      this.#config.maxDateFromNow &&
      typeof this.#config.maxDateFromNow === "number"
    ) {
      return new Date().fp_incr(this.#config.maxDateFromNow);
    }
    return undefined;
  }

  saveAndFill = task({ drop: true }, async (value) => {
    const endQuestion = this.args.field.document.findField(
      this.#config.question,
    );
    const endDate = DateTime.fromISO(value)
      .plus({ days: this.#config.delta })
      .toISODate();

    endQuestion.answer.value = endDate;
    await endQuestion.save.perform();
    await this.args.onSave(value);
  });
}
