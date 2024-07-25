import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";

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

      if (this.data.value) {
        this.reset();
      }

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
