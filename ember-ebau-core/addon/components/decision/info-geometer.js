import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

export default class DecisionInfoGeometerComponent extends Component {
  @service intl;
  @service store;

  fetchGeometer = task(async (instanceId) => {
    await Promise.resolve();

    const instance =
      this.store.peekRecord("instance", instanceId) ??
      (await this.store.findRecord("instance", instanceId));
    const municipality = instance.activeService;

    if (!municipality) {
      return;
    }

    const geometer = await this.store.query("public-service", {
      provider_for: `geometer;${municipality.id}`,
    });

    return geometer.firstObject;
  });

  geometer = trackedTask(this, this.fetchGeometer, () => [
    this.args.context.instanceId,
  ]);

  get geometerName() {
    return this.geometer.value?.name;
  }

  get geometerInfo() {
    return htmlSafe(
      this.intl.t("decision.info.geometer", {
        geometer: this.geometerName,
      }),
    );
  }

  get staticQuestionContent() {
    return htmlSafe(this.args.field.raw.question.staticContent);
  }
}
