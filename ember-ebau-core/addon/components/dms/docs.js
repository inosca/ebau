import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { trackedFunction } from "reactiveweb/function";
import { cached } from "tracked-toolbox";

import { parseNested } from "ember-ebau-core/utils/dms";

export default class DmsDocsComponent extends Component {
  @service intl;
  @service fetch;
  @service notification;

  @tracked expand = false;
  @tracked search = "";

  docs = trackedFunction(this, async () => {
    const response = await this.fetch.fetch("/api/v1/dms-placeholders-docs", {
      headers: { accept: "application/json" },
    });

    return await response.json();
  });

  @cached
  get allPlaceholders() {
    if (!this.docs.value) {
      return [];
    }

    return Object.entries(this.docs.value)
      .map(([name, docs]) => this.parse(name, docs))
      .filter(Boolean)
      .sort((a, b) => a.placeholder.localeCompare(b.placeholder));
  }

  get placeholders() {
    if (!this.search) return this.allPlaceholders;

    return this.allPlaceholders.filter(({ placeholder }) =>
      placeholder.toLowerCase().includes(this.search.toLowerCase()),
    );
  }

  parse(name, docs) {
    if (!docs.description) {
      return null;
    }

    let value = this.args.data?.[name] ?? "";

    const locale = this.intl.primaryLocale.split("-")[0];
    const isComplex = Object.keys(docs.nested_aliases).length > 0;
    const isLink = /^http(s)?:\/\//.test(value);
    const isImage = /^data:image\//.test(value);

    if (isComplex && value) {
      value = JSON.stringify(
        parseNested(value, docs.nested_aliases, locale),
        null,
        "  ",
      );
    }

    return {
      placeholder: docs.aliases[0][locale],
      description: docs.description[locale],
      value,
      isComplex,
      isLink,
      isImage,
    };
  }

  @action
  copyToClipboard(placeholder) {
    navigator.clipboard.writeText(`{{ ${placeholder.placeholder} }}`);
    this.notification.success(
      this.intl.t("dms.docs.copy-to-clipboard-success"),
    );
  }
}
