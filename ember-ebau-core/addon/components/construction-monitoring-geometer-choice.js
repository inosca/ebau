import { service } from "@ember/service";
import CfFieldInputRadio from "@projectcaluma/ember-form/components/cf-field/input/radio";
import { task } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";

export default class ConstructionMonitoringGeometerChoiceComponent extends CfFieldInputRadio {
  @service store;

  isGeometerOption = (option) => {
    return option.slug.endsWith("-geometer");
  };

  fetchGeometer = task(async (instanceId) => {
    await Promise.resolve();

    const geometer = await this.store.query("public-service", {
      provider_for_instance_municipality: `geometer;${instanceId}`,
    });

    return geometer[0];
  });

  geometer = trackedTask(this, this.fetchGeometer, () => [
    this.args.context.instanceId,
  ]);

  get geometerName() {
    return this.geometer.value?.name;
  }
}
