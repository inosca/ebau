import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { trackedFunction } from "reactiveweb/function";
import { dedupeTracked } from "tracked-toolbox";

import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class CommunicationTopicListComponent extends Component {
  @service router;
  @service store;
  @service intl;
  @service ebauModules;

  get showResponsibleServiceUsers() {
    return !this.args.instanceId && !this.ebauModules.isApplicant;
  }

  @tracked responsiblePerson;

  responsibleServiceUsers = trackedFunction(this, async () => {
    await Promise.resolve();
    if (!this.showResponsibleServiceUsers) {
      return [];
    }

    const users = await this.store.query("user", {
      responsible_for_instances: true,
      sort: "name",
    });

    return [
      ...users,
      {
        id: "nobody",
        fullName: this.intl.t("cases.filters.responsibleServiceUser-nobody"),
      },
    ];
  });

  @dedupeTracked topicsFilter = "all";
  @dedupeTracked page = 1;

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

  get colspan() {
    if (this.args.instanceId) {
      return 4;
    }

    return this.ebauModules.isApplicant ? 5 : 6;
  }

  topics = paginatedQuery(this, "communications-topic", () => ({
    has_unread: this.showOnlyUnread,
    instance: this.args.instanceId,
    include: "instance",
    responsible_service_user: this.responsiblePerson?.id,
    page: {
      number: this.page,
      size: 20,
    },
    order: "-created_at",
  }));

  @action
  transitionToTopic(topic) {
    const instanceId = topic.get("instance.id");
    const routeName = this.ebauModules.resolveModuleRoute(
      "communications",
      "detail",
    );

    if (this.ebauModules.applicationName === "camac-ng") {
      if (
        this.router.currentRouteName ===
        this.ebauModules.resolveModuleRoute(
          "communications-global",
          "communications-global",
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
  updateTopicsFilter(value) {
    this.topicsFilter = value;
    this.page = 1;
  }

  @action
  updateResponsibleUserFilter(value) {
    this.responsiblePerson = value;
    this.page = 1;
  }

  @action
  updatePage() {
    if (this.topics.hasMore && !this.topics.isLoading) {
      this.page += 1;
    }
  }
}
