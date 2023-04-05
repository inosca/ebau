import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";
import { findAll } from "ember-data-resources";
import { trackedFunction } from "ember-resources/util/function";

export default class CommunicationNewTopicComponent extends Component {
  @service store;
  @service router;
  @service notification;
  @service intl;

  services = findAll(this, "service");

  topic = trackedFunction(this, async () => {
    try {
      const instance =
        typeof parseInt(this.args.instance) === "number"
          ? this.store.peekRecord("instance", this.args.instance) ??
            (await this.store.findRecord("instance", this.args.instance))
          : this.args.instance;
      return this.store.createRecord("communications-topic", {
        instance,
      });
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("communications.new.fetchError"));
      this.router.transitionTo(this.args.listRoute);
    }
  });

  get saveDisabled() {
    return !(
      this.topic.value?.involvedEntities?.length && this.topic.value?.subject
    );
  }

  @action
  setInvolvedEntities(services) {
    this.topic.value.involvedEntities = services.map((service) => ({
      id: service.id,
      name: service.name,
    }));
  }

  @action
  preventDefault(event) {
    event.preventDefault();
  }

  createTopic = task(async (messageText, files) => {
    try {
      const topic = await this.topic.value.save();
      const message = this.store.createRecord("communications-message", {
        body: messageText,
        topic,
      });
      await message.save();
      console.log(files);
      this.router.transitionTo(this.args.detailRoute, topic);
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("communications.new.saveError"));
    }
  });
}
