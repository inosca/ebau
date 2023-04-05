import { assert } from "@ember/debug";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dedupeTracked } from "tracked-toolbox";

import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class CommunicationTopicListComponent extends Component {
  @service router;

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
    return this.args.instance ? 3 : 4;
  }

  topics = paginatedQuery(this, "communications-topic", () => ({
    has_unread: this.showOnlyUnread,
    instance: this.args.instance,
    include: "instance",
    page: {
      number: this.page,
      size: 20,
    },
  }));

  constructor(owner, args) {
    super(owner, args);
    assert(
      "Must specify argument @detailRoute on <TopicList/> component.",
      typeof args.detailRoute === "string"
    );
    if (args.instance) {
      assert(
        "Must specify argument @newRoute on <TopicList/> component.",
        typeof args.newRoute === "string"
      );
    }
  }

  @action
  transitionToTopic(topic) {
    this.router.transitionTo(this.args.detailRoute, topic);
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
