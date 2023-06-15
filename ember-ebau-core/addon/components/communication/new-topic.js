import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

export default class CommunicationNewTopicComponent extends Component {
  @service store;
  @service router;
  @service fetch;
  @service notification;
  @service ebauModules;
  @service intl;
  @service abilities;

  @tracked message;

  get topic() {
    return this.topicResource.value;
  }

  get services() {
    return this.topic?.get("instance.involvedServices");
  }

  get selectableServices() {
    if (!this.topic) {
      return null;
    }

    // Without current service
    const services = this.services
      ?.filter(
        (service) =>
          parseInt(service.id) !== parseInt(this.ebauModules.serviceId)
      )
      .map((service) => ({ id: service.get("id"), name: service.name }));

    // We are a Leitbehörde so we add the applicant to the list
    if (this.abilities.can("involve applicant on topic", this.topic)) {
      services.push({
        id: "APPLICANT",
        name: this.intl.t("communications.new.applicant"),
      });
    }

    return services;
  }

  get saveDisabled() {
    return !(
      this.topic?.involvedEntities?.length &&
      this.topic?.subject &&
      this.message?.body
    );
  }

  topicResource = trackedFunction(this, async () => {
    try {
      const instance = await this.store.findRecord(
        "instance",
        this.args.instanceId,
        { include: "involved_services,active_service", reload: true }
      );
      const topic = this.store.createRecord("communications-topic", {
        instance,
      });

      // Applicant can only select instance active service
      if (this.abilities.cannot("involve entities on topic")) {
        topic.involvedEntities = [
          {
            id: instance.get("activeService.id"),
            name: instance.get("activeService.name"),
          },
        ];
      }

      this.message = this.store.createRecord("communications-message", {
        topic,
      });
      return topic;
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("communications.new.fetchError"));
    }
  });

  createTopic = task(async () => {
    try {
      const topic = await this.topic.save();
      await this.message.send();

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute("communications", "detail"),
        topic.id
      );
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("communications.new.saveError"));
    }
  });

  @action
  setInvolvedEntities(services) {
    this.topic.involvedEntities = services;
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
}
