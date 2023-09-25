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
  @tracked content = "";

  data = trackedTask(this, this.fetchData, () => [this.args.type]);

  @action
  startEdit() {
    this._oldContent = this.content;
    this.edit = true;
  }

  @action
  cancelEdit() {
    this.content = this._oldContent;
    this.edit = false;
  }

  @dropTask
  *save() {
    try {
      const staticContent = yield this.store.query("static-content", {
        slug: this.args.type,
      });

      if (staticContent.content.length === 0) {
        const newStaticContent = this.store.createRecord("static-content", {
          slug: this.args.type,
          content: this.content,
        });
        yield newStaticContent.save();
      } else {
        staticContent.firstObject.content = this.content;
        yield staticContent.save();
      }

      this.edit = false;
    } catch (error) {
      this.notification.danger(this.intl.t("static-content.saveError"));
    }
  }

  @dropTask
  *fetchData() {
    try {
      yield Promise.resolve();
      const response = yield this.store.query("static-content", {
        slug: this.args.type,
      });

      this.content = response.firstObject.content;
    } catch (error) {
      this.notification.danger(this.intl.t("static-content.loadError"));
    }
  }
}
