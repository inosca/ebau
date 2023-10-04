import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

export default class StaticContentComponent extends Component {
  @service store;
  @service intl;
  @service notification;

  @tracked edit = false;

  data = trackedTask(this, this.fetchData, () => [this.args.type]);

  @dropTask
  *fetchData() {
    try {
      yield Promise.resolve();
      const response = yield this.store.query("static-content", {
        slug: this.args.type,
      });

      return (
        response.firstObject ||
        this.store.createRecord("static-content", {
          slug: this.args.type,
        })
      );
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("static-content.loadError"));
    }
  }

  @action
  reset() {
    this.edit = false;
    this.data.value.rollbackAttributes();
  }

  @dropTask
  *save() {
    try {
      yield this.data.value.save();
      this.edit = false;
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("static-content.saveError"));
    }
  }
}
