import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency-decorators";
import { useTask } from "ember-resources";

import saveDashboardContent from "caluma-portal/gql/mutations/save-dashboard-content.graphql";
import getDashboardContent from "caluma-portal/gql/queries/get-dashboard-content.graphql";

export default class BeDashboardComponent extends Component {
  @queryManager apollo;

  @service intl;
  @service session;
  @service notification;

  @tracked edit = false;
  @tracked content = "";

  data = useTask(this, this.fetchData, () => [this.slug]);

  get slug() {
    return `${this.args.page}-${this.session.language}`;
  }

  @action
  startEdit() {
    this._oldContent = this.content;
    this.edit = true;
  }

  @action
  cancelEdit() {
    this.content = this._oldContent;
    this.edit = false;
  }

  @dropTask
  *save() {
    try {
      yield this.apollo.mutate({
        mutation: saveDashboardContent,
        variables: {
          document: decodeId(this.documentId),
          page: this.slug,
          content: this.content,
        },
      });

      this.edit = false;
    } catch (error) {
      this.notification.danger(this.intl.t("dashboard.save-error"));
    }
  }

  @dropTask
  *fetchData() {
    try {
      const response = yield this.apollo.query({
        query: getDashboardContent,
        variables: { page: this.slug },
      });

      this.documentId = response.allDocuments.edges[0].node.id;
      this.content =
        response.allDocuments.edges[0].node.answers.edges[0]?.node.value ?? "";
    } catch (error) {
      this.notification.danger(this.intl.t("dashboard.load-error"));
    }
  }
}
