import Controller from "@ember/controller";
import { action, computed } from "@ember/object";
import { inject as service } from "@ember/service";

export default class InstancesEditPersonalienProjektverfasserPlanerController extends Controller {
  @service("question-store") questionStore;

  @computed("model.instance.fields.@each")
  get questionActive() {
    return (
      this.model.meta.editable.includes("form") &&
      this.model.instance.fields.findBy("name", "bauherrschaft")
    );
  }

  @action
  async copyQuestionValue() {
    const question = await this.questionStore.peek(
      "projektverfasser-planer",
      this.model.instance.id
    );
    question.set(
      "model.value",
      question
        .getWithDefault("model.value", [])
        .pushObjects(this.bauherrschaftValue)
        .uniqBy("uuid")
    );
    await this.questionStore.saveQuestion.perform(question);
  }
}
