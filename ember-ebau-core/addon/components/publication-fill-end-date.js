import Component from "@glimmer/component";
import { task } from "ember-concurrency";
import { DateTime } from "luxon";

export default class PublicationFillEndDate extends Component {
  get #config() {
    return this.args.field.raw.question.meta["fill-end-date"] ?? {};
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
