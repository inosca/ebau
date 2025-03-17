import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { validatePresence } from "ember-changeset-validations/validators";
import { task } from "ember-concurrency";
import { query } from "ember-data-resources";
import { pluralize } from "ember-inflector";

export default class SanctionsEditComponent extends Component {
  validations = {
    name: validatePresence(true),
    assignedService: validatePresence(true),
    controlStep: validatePresence(true),
  };

  @service ebauModules;
  @service router;
  @service notification;
  @service intl;
  @service store;

  get className() {
    return this.args.model.constructor.modelName;
  }

  get parentRoute() {
    return this.ebauModules.resolveModuleRoute(
      pluralize(this.className),
      "index",
    );
  }

  saveMessage(type) {
    const i18nPrefix = this.className.replace("-", "");
    return `${i18nPrefix}.notification.${type}.save`;
  }

  get controlSteps() {
    return ["baufreigabe", "realisierung", "endabnahme", "variabel"].map(
      (key) => ({ key, label: this.intl.t(`sanction.controlStep.${key}`) }),
    );
  }

  availableServices = query(this, "service", () => ({
    filter: {
      available_in_sanctions: true,
    },
  }));

  get options() {
    return this.availableServices.records ?? [];
  }

  save = task(async (changeset) => {
    try {
      await changeset.save();
      this.notification.success(this.intl.t(this.saveMessage("success")));
      this.router.transitionTo(this.parentRoute);
    } catch {
      this.notification.danger(this.intl.t(this.saveMessage("error")));
      this.store.unloadRecord(changeset.data);
    }
  });

  @action
  async cancel(changeset) {
    changeset.data.rollbackAttributes();
    this.router.transitionTo(this.parentRoute);
  }
}
