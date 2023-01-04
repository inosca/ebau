import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { cached } from "tracked-toolbox";

import {
  ALL_PLACEHOLDERS,
  COMPLEX_PLACEHOLDERS,
} from "ember-ebau-core/utils/dms";

export default class DmsDocsComponent extends Component {
  @service intl;

  @tracked expand = false;
  @tracked search = "";

  @cached
  get allPlaceholders() {
    const complexPlaceholders = COMPLEX_PLACEHOLDERS.map(
      (placeholder) => placeholder.split("[]")[0]
    );

    return ALL_PLACEHOLDERS.filter((placeholder) =>
      this.intl.exists(`dms.docs.placeholders.${placeholder}-placeholder`)
    ).map((placeholder) => {
      const value = this.args.data?.[placeholder] ?? "";
      const isComplex = complexPlaceholders.includes(placeholder);
      const isLink = /^http(s)?:\/\//.test(value);

      return {
        placeholder: this.intl.t(
          `dms.docs.placeholders.${placeholder}-placeholder`
        ),
        description: this.intl.t(
          `dms.docs.placeholders.${placeholder}-description`
        ),
        value: isComplex ? JSON.stringify(value, null, "  ") : value,
        isComplex,
        isLink,
      };
    });
  }

  get placeholders() {
    if (!this.search) return this.allPlaceholders;

    return this.allPlaceholders.filter(({ placeholder }) =>
      placeholder.toLowerCase().includes(this.search.toLowerCase())
    );
  }
}
