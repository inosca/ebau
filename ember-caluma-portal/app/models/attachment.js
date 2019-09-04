import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import filesize from "filesize";
import { dropTask, lastValue } from "ember-concurrency-decorators";
import { saveAs } from "file-saver";
import gql from "graphql-tag";
import { ObjectQueryManager } from "ember-apollo-client";

export default class Attachment extends Model.extend(ObjectQueryManager) {
  @service fetch;
  @service intl;
  @service notification;

  @attr("date") date;
  @attr("string") mimeType;
  @attr("string") name;
  @attr("string") path;
  @attr("string") size;
  @attr() context;
  @hasMany("attachment-section") attachmentSections;
  @belongsTo("instance", { async: false }) instance;

  @computed("size")
  get filesize() {
    return filesize(this.size);
  }

  @lastValue("_tags") tags;
  @computed("context.tags.[]")
  get _tags() {
    const task = this.fetchTags;

    task.perform();

    return task;
  }

  @dropTask
  *fetchTags() {
    if (!this.context.tags) return [];

    const raw = yield this.apollo.query(
      {
        query: gql`
          query($slugs: [String]!) {
            allQuestions(slugs: $slugs) {
              edges {
                node {
                  slug
                  label
                }
              }
            }
          }
        `,
        variables: { slugs: this.context.tags }
      },
      "allQuestions.edges"
    );

    return this.context.tags
      .map(slug => {
        const tag = raw.find(({ node }) => node.slug === slug);

        return tag && tag.node;
      })
      .filter(Boolean);
  }

  @dropTask
  *download() {
    try {
      const response = yield this.fetch.fetch(`${this.path}`, {
        mode: "cors",
        headers: {
          accept: undefined,
          "content-type": undefined
        }
      });

      const file = yield response.blob();

      saveAs(file, this.name, { type: file.type });

      this.notification.success(this.intl.t("documents.downloadSuccess"));
    } catch (e) {
      /* eslint-disable-next-line no-console */
      console.error(e);
      this.notification.danger(this.intl.t("documents.downloadError"));
    }
  }
}
