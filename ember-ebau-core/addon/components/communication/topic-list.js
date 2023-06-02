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
    this.router.transitionTo(
      this.ebauModules.resolveModuleRoute(
        this.args.instanceId ? "communications" : "communications-global",
        this.args.detailRoute
      ),
      topic.id
    );
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
