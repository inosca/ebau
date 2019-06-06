import Component from "@ember/component";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";

import gql from "graphql-tag";

const GROUP = 6;

const documentsToSign = [
  "situationsplan-dokument",
  "grundriss-dokument",
  "schnitt-dokument",
  "fassaden-ansichten-dokument",
  "umgebungsplan-dokument",
  "werkleitungsplan-dokument",
  "brandschutzplan-dokument",
  "kanalisationskatasterplan-dokument",
  "grundstueckentwaesserungsplan-dokument",
  "schutzraum-dokument",
  "bewehrungsplan-bewehrungsliste-dokument",
  "fassadenplan-reklamestandort-dokument",
  "skizze-der-reklame-mit-farbangaben-dokument"
];

export default Component.extend({
  apollo: service(),
  fetch: service(),

  didReceiveAttrs() {
    this._super(...arguments);

    this.tags.perform();
  },

  tags: task(function*() {
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

    const response = yield this.fetch.fetch(
      `/api/v1/attachments?group=${GROUP}&instance=${instanceId}`
    );

    const { data } = yield response.json();

    const tags = [
      ...new Set(
        data.reduce(
          (flat, attachment) => [
            ...flat,
            ...attachment.attributes.context.tags
          ],
          []
        )
      )
    ];

    const tagsToSign = tags.filter(tag => documentsToSign.includes(tag));

    return tagsToSign
      .map(slug => this.field.document.findField(`root.6-dokumente.${slug}`))
      .map(field => field.question.label);
  })
});
