import Component from "@ember/component";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";
import EmberObject, { computed, getWithDefault } from "@ember/object";
import { filterBy, reads } from "@ember/object/computed";
import { A } from "@ember/array";
import { all } from "rsvp";
import { isBlank } from "@ember/utils";
import { getOwner } from "@ember/application";

import gql from "graphql-tag";
import filesize from "filesize";
import download from "downloadjs";
import moment from "moment";

const DEFAULT_CATEGORY = "weitere-unterlagen";
const GROUP = 6;

const Attachment = EmberObject.extend({
  fetch: service(),
  notification: service(),
  intl: service(),

  name: reads("attributes.name"),
  path: reads("attributes.path"),
  size: computed("attributes.size", function() {
    return filesize(this.attributes.size);
  }),
  date: computed("attributes.date", function() {
    return moment(this.attributes.date);
  }),
  tags: computed("attributes.meta.tags", function() {
    return getWithDefault(this, "attributes.meta.tags", []).map(slug => {
      const field = this.document.fields.find(f => f.question.slug === slug);

      return (field && field.question.label) || slug;
    });
  }),

  download: task(function*() {
    try {
      let response = yield this.fetch.fetch(`${this.path}?group=${GROUP}`, {
        mode: "cors",
        headers: {
          accept: undefined,
          "content-type": undefined
        }
      });

      let file = yield response.blob();

      download(file, this.name, file.type);

      this.notification.success(this.intl.t("documents.downloadSuccess"));
    } catch (e) {
      /* eslint-disable-next-line no-console */
      console.error(e);
      this.notification.danger(this.intl.t("documents.downloadError"));
    }
  })
});

export default Component.extend({
  intl: service(),
  apollo: service(),
  fetch: service(),
  notification: service(),

  didReceiveAttrs() {
    this._super(...arguments);

    this.data.perform();
  },

  data: task(function*() {
    const instanceId = yield this.apollo.query(
      {
        query: gql`
          query($caseId: ID!) {
            allWorkItems(case: $caseId, task: "fill-form") {
              edges {
                node {
                  case {
                    meta
                  }
                }
              }
            }
          }
        `,
        variables: { caseId: this.context.caseId }
      },
      "allWorkItems.edges.firstObject.node.case.meta.camac-instance-id"
    );

    this.set("instanceId", instanceId);

    const response = yield this.fetch.fetch(
      `/api/v1/attachments?group=${GROUP}&instance=${instanceId}`
    );

    const { data } = yield response.json();

    return data.map(a =>
      Attachment.create(
        getOwner(this).ownerInjection(),
        Object.assign(a, { document: this.document })
      )
    );
  }),

  allVisibleTags: computed("document.fields.@each.{hidden,isNew}", function() {
    return this.document.fields.filter(f => !f.hidden).filter(f => f.isNew);
  }),

  allRequiredTags: filterBy("allVisibleTags", "optional", false),
  allOptionalTags: filterBy("allVisibleTags", "optional", true),

  requiredTags: computed("allRequiredTags.[]", function() {
    return this.allRequiredTags.reduce((tree, tag) => {
      const category = tag.question.meta.documentCategory || DEFAULT_CATEGORY;

      return Object.assign(tree, {
        [category]: [...(tree[category] || []), tag]
      });
    }, {});
  }),

  optionalTags: computed("allOptionalTags.[]", "intl.locale", function() {
    return this.allOptionalTags.reduce((grouped, tag) => {
      const category = this.intl.t(
        `documents.tags.${tag.question.meta.documentCategory ||
          DEFAULT_CATEGORY}`
      );

      let group = grouped.find(g => g.groupName === category);

      if (!group) {
        group = {
          groupName: category,
          options: []
        };

        grouped.push(group);
      }

      group.options.push(tag);

      return grouped;
    }, []);
  }),

  selectedRequiredTags: A([]),
  selectedOptionalTags: A([]),
  allSelectedTags: computed(
    "selectedRequiredTags.[]",
    "selectedOptionalTags.[]",
    function() {
      return [
        ...new Set([...this.selectedRequiredTags, ...this.selectedOptionalTags])
      ];
    }
  ),

  saveFile: task(function*() {
    const formData = new FormData();

    formData.append("instance", this.instanceId);
    formData.append(
      "meta",
      JSON.stringify({
        tags: this.allSelectedTags.map(
          ({ question: { slug, label } }) => slug || label
        )
      })
    );
    formData.append("group", GROUP);
    formData.append("path", this.file.blob, this.file.name);

    yield this.fetch.fetch("/api/v1/attachments", {
      method: "post",
      body: formData,
      headers: {
        "content-type": undefined
      }
    });
  }),

  saveFields: task(function*() {
    const fields = this.allSelectedTags.filter(
      t => t.question.slug && t.question.__typename === "MultipleChoiceQuestion"
    );

    yield all(
      fields.map(async field => {
        field.set(
          "answer.value",
          field.get(
            "question.multipleChoiceOptions.edges.firstObject.node.slug"
          )
        );

        await field.save.perform();
      })
    );
  }),

  save: task(function*() {
    try {
      yield this.saveFile.perform();
      yield this.saveFields.perform();

      this._reset();

      yield this.data.perform();

      this.notification.success(this.intl.t("documents.uploadSuccess"));
    } catch (e) {
      /* eslint-disable-next-line no-console */
      console.error(e);
      this.notification.danger(this.intl.t("documents.uploadError"));
    }
  }),

  _reset() {
    this.setProperties({
      file: null,
      selectedOptionalTags: A([]),
      selectedRequiredTags: A([])
    });
  },

  actions: {
    reset() {
      this._reset();
    },

    createCustomTag(select, e) {
      if (
        e.keyCode === 13 &&
        select.isOpen &&
        !select.highlighted &&
        !isBlank(select.searchText)
      ) {
        const fields = this.allSelectedTags;

        if (!fields.map(f => f.question.slug).includes(select.searchText)) {
          this.set("selectedOptionalTags", [
            ...this.selectedOptionalTags,
            { question: { label: select.searchText } }
          ]);
        }
      }
    },

    updateSelectedRequiredTags(tag) {
      const selectedRequiredTags = new Set(this.selectedRequiredTags);

      selectedRequiredTags.delete(tag) || selectedRequiredTags.add(tag);

      this.set("selectedRequiredTags", [...selectedRequiredTags]);
    }
  }
});
