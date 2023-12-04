import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";
import { DateTime } from "luxon";

import InstanceAclValidations from "../../validations/instance-acl-form";

export default class CreateAclModalComponent extends Component {
  @service intl;
  @service notification;
  @service store;

  validations = InstanceAclValidations;
  today = DateTime.now().toISODate();

  constructor(...args) {
    super(...args);

    // pre-fetch the available services to mend the laggy behavior of emper power select
    this.availableServices;
  }

  get availableServices() {
    return this.store.findAll("public-service");
  }

  get availableAccessLevels() {
    // TODO: restrict to manually configurable access-levels
    return this.store.findAll("access-level");
  }

  createAcl = task({ drop: true }, async (changeset) => {
    try {
      const instance = await this.store.findRecord(
        "instance",
        this.args.instanceId,
      );
      const service = await this.store.findRecord(
        "service",
        changeset.service.id,
      );
      // set end time to last hour of the day
      const endTime = DateTime.fromJSDate(changeset.pendingData.endTime).set({
        hour: 23,
        minute: 59,
        second: 59,
      });
      const acl = this.store.createRecord("instance-acl", {
        ...changeset.pendingData,
        endTime,
        // TODO: hardcoded until further grant types are allowed for manual creation
        grantType: "SERVICE",
        instance,
        service,
      });
      await acl.save();

      //reset inputs
      changeset.rollback();

      this.args.afterCreate();
      // close the modal dialog
      this.args.onHide();
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("permissions.saveError"));
    }
  });
}
