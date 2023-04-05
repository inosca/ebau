import { assert } from "@ember/debug";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";
import { findAll } from "ember-data-resources";
import { trackedFunction } from "ember-resources/util/function";

export default class CommunicationNewTopicComponent extends Component {
  @service store;
  @service session;
  @service router;
  @service notification;
  @service intl;

  @tracked message;

  services = findAll(this, "service");

  get servicesWithoutCurrent() {
    const currentActiveServiceId = this.session.groups
      .find((group) => group.id === this.session.group)
      ?.belongsTo("service")
      .id();

    return this.services.records?.filter(
      (service) => service.id !== currentActiveServiceId
    );
  }

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
      this.topic.value?.involvedEntities?.length &&
      this.topic.value?.subject &&
      this.message?.body
    );
  }

  constructor(owner, args) {
    super(owner, args);
    assert(
      "Must specify argument @detailRoute on <NewTopic/> component.",
      typeof args.detailRoute === "string"
    );
    assert(
      "Must specify argument @listRoute on <NewTopic/> component.",
      typeof args.listRoute === "string"
    );
    assert(
      "Must specify argument @instance on <NewTopic/> component.",
      typeof args.instance === "string"
    );

    this.message = this.store.createRecord("communications-message", {
      topic: this.topic.value,
    });
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

  @action
  updateMessage(body) {
    this.message.body = body;
  }

  @action
  updateFiles(files) {
    this.message.filesToSave = files;
  }

  createTopic = task(async () => {
    try {
      const topic = await this.topic.value.save();
      await this.message.save();
      this.router.transitionTo(this.args.detailRoute, topic);
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("communications.new.saveError"));
    }
  });
}
