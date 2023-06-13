import { getOwner } from "@ember/application";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dedupeTracked } from "tracked-toolbox";

import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class CommunicationTopicListComponent extends Component {
  @service router;
  @service ebauModules;

  @dedupeTracked topicsFilter = "all";
  @dedupeTracked page = 1;
  @dedupeTracked element;

  get showOnlyUnread() {
    switch (this.topicsFilter) {
      case "read": {
        return false;
      }
      case "unread": {
        return true;
      }
      default: {
        return undefined;
      }
    }
  }

  get topicsListHidden() {
    return parseInt(this.page) === 1 && this.topics.isLoading;
  }

  get colspan() {
    return this.args.instanceId ? 3 : 4;
  }

  topics = paginatedQuery(this, "communications-topic", () => ({
    has_unread: this.showOnlyUnread,
    instance: this.args.instanceId,
    include: "instance",
    page: {
      number: this.page,
      size: 20,
    },
    order: "-created_at",
  }));

  @action
  transitionToTopic(topic) {
    const applicationName = getOwner(this).application.modulePrefix;

    const instanceId = topic.get("instance.id");
    const routeName = this.ebauModules.resolveModuleRoute(
      "communications",
      "detail"
    );

    if (applicationName === "camac-ng") {
      if (
        this.router.currentRouteName ===
        this.ebauModules.resolveModuleRoute(
          "communications-global",
          "communications-global"
        )
      ) {
        // If we are on the global page in ember-camac-ng, we need to use a hard
        // transition to the correct instance resource with the ember hash appended
        const url = [
          "/index/redirect-to-instance-resource/instance-id/",
          instanceId,
          "?instance-resource-name=communication",
          "&ember-hash=",
          this.router.urlFor(routeName, topic.id),
        ].join("");

        location.assign(url);
      } else {
        // ember-camac-ng does not have the instance ID in the ember url
        this.router.transitionTo(routeName, topic.id);
      }
    } else {
      this.router.transitionTo(routeName, instanceId, topic.id);
    }
  }

  @action
  scrollToFirst() {
    this.element.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  @action
  updateFilter(value) {
    this.topicsFilter = value;
    this.page = 1;
    this.element = null;
  }

  @action
  updatePage() {
    if (this.topics.hasMore && !this.topics.isLoading) {
      this.page += 1;
    }
  }

  @action
  setElement(element) {
    if (!this.element) {
      this.element = element;
    }
  }
}
