import { assert } from "@ember/debug";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dedupeTracked } from "tracked-toolbox";

import paginatedQuery from "ember-ebau-core/resources/paginated-query";

export default class CommunicationTopicListComponent extends Component {
  @service router;

  @dedupeTracked showOnlyUnread = false;
  @dedupeTracked page = 1;
  @dedupeTracked element;

  get topicsListHidden() {
    return parseInt(this.page) === 1 && this.topics.isLoading;
  }

  get colspan() {
    return this.args.instance ? 3 : 4;
  }

  topics = paginatedQuery(this, "communications-topic", () => ({
    has_unread: this.showOnlyUnread,
    instance: this.args.instance,
    include: "instance,involved_entities",
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
  transitionToTopic(instanceId) {
    this.router.transitionTo(this.args.detailRoute, instanceId);
  }

  @action
  scrollToFirst() {
    this.element.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  @action
  updateFilter(value) {
    this.showOnlyUnread = value;
    this.page = 1;
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
