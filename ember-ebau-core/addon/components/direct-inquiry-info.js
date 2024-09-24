import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import isDirectInquiryQuery from "ember-ebau-core/gql/queries/is-direct-inquiry.graphql";

export default class DirectInquiryInfoComponent extends Component {
  @queryManager apollo;

  #isDirect = trackedFunction(this, async () => {
    const response = await this.apollo.query(
      {
        query: isDirectInquiryQuery,
        variables: {
          documentId: decodeId(this.args.context.inquiry.document.id),
        },
      },
      "allDocuments.totalCount",
    );

    return response > 0;
  });

  get isDirect() {
    return this.#isDirect.value ?? false;
  }
}
