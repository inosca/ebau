import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

export default class CommunicationNewTopicComponent extends Component {
  @service store;
  @service session;
  @service router;
  @service notification;
  @service intl;

  @tracked message;

  get topic() {
    return this.topicResource.value;
  }

  get services() {
    return this.topic?.get("instance.involvedServices");
  }

  get activeServiceId() {
    return this.session.groups
      .find((group) => group.id === this.session.group)
      ?.belongsTo("service")
      .id();
  }

  get activeInstanceService() {
    return this.topic?.get("instance.activeService");
  }

  // Leitbehörde
  get isActiveInstanceService() {
    return this.activeServiceId === this.activeInstanceService?.get("id");
  }

  get selectableServices() {
    if (!this.topic) {
      return null;
    }

    if (!this.session.isInternal) {
      // Applicant can only select instance active service
      return [
        {
          id: this.activeInstanceService.get("id"),
          name: this.activeInstanceService.get("name"),
        },
      ];
    }

    // Without current service
    const services = this.services
      ?.filter((service) => service.id !== this.activeServiceId)
      .map((service) => ({ id: service.get("id"), name: service.name }));

    // We are a Leitbehörde so we add the applicant to the list
    if (this.isActiveInstanceService) {
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
      this.message = this.store.createRecord("communications-message", {
        topic: this.topic,
      });
      return this.store.createRecord("communications-topic", {
        instance,
      });
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("communications.new.fetchError"));
    }
  });

  createTopic = task(async () => {
    try {
      const topic = await this.topic.save();
      await this.message.save();
      this.router.transitionTo(this.args.detailRoute, topic);
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
