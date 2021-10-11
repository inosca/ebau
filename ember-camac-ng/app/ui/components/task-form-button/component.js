import { inject as controller } from "@ember/controller";
import { action } from "@ember/object";
import Component from "@glimmer/component";

import confirm from "camac-ng/utils/confirm";

export default class TaskFormButtonComponent extends Component {
  @controller("task-form") taskFormController;

  @action
  async beforeMutate(validateFn) {
    if (!(await validateFn())) {
      return false;
    }

    const text = this.args.field.question.staticContent;

    if (!text) {
      return true;
    }

    return confirm(text);
  }

  @action
  refreshWorkItem() {
    this.taskFormController?.fetchWorkItem.perform();
  }
}
