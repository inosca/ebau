import Controller from "@ember/controller";
import { action, computed } from "@ember/object";
import { inject as service } from "@ember/service";

export default class InstancesEditPersonalienBauherrschaftController extends Controller {
  @service("question-store") questionStore;

  @computed("model.instance.fields.@each")
  get questionActive() {
    return (
      this.model.meta.editable.includes("form") &&
      this.model.instance.fields.findBy("name", "grundeigentumerschaft")
    );
  }

  @action
  async copyQuestionValue() {
    const question = await this.questionStore.peek(
      "bauherrschaft",
      this.model.instance.id
    );
    question.set(
      "model.value",
      question
        .getWithDefault("model.value", [])
        .pushObjects(this.grundeigentumerschaftValue)
        .uniqBy("uuid")
    );
    await this.questionStore.saveQuestion.perform(question);
  }
}
