import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { trackedFunction } from "reactiveweb/function";
import { cached } from "tracked-toolbox";

/**
 * Recursively filter complex placeholder data (one item of an array value)
 * based on the available aliases in the given language.
 *
 * const item = {
 *   date: 1,
 *   datum: 1,
 *   opposing: [
 *     {
 *       address: 1,
 *       adresse: 1,
 *     },
 *     {
 *       address: 1,
 *       adresse: 1,
 *     },
 *   ],
 *   einsprechende: [
 *     {
 *       address: 1,
 *       adresse: 1,
 *     },
 *     {
 *       address: 1,
 *       adresse: 1,
 *     },
 *   ],
 * };
 *
 * const aliases = {
 *   date: [{ de: "datum" }],
 *   opposing: [{ de: "einsprechende" }],
 *   "opposing.address": [{ de: "adresse" }],
 * };
 *
 * const result = parseNested(item, aliases, "de")
 *
 * Will return the following structure:
 *
 * const result =  {
 *   datum: 1,
 *   einsprechende: [
 *     {
 *       adresse: 1,
 *     },
 *     {
 *       adresse: 1,
 *     },
 *   ],
 * };
 */
function parseNested(item, aliases, locale) {
  return Object.entries(item).reduce((prev, [key, value]) => {
    const alias = aliases[key]?.[0]?.[locale];

    const doubleNestedRe = new RegExp(`^${key}.`);
    const doubleNested = Object.entries(aliases).reduce(
      (_prev, [nestedKey, nestedAliases]) => {
        if (nestedKey.search(doubleNestedRe) < 0) {
          return _prev;
        }

        return {
          ..._prev,
          [nestedKey.replace(doubleNestedRe, "")]: nestedAliases,
        };
      },
      {},
    );

    if (Object.keys(doubleNested).length) {
      value = value.map((v) => parseNested(v, doubleNested, locale));
    }

    if (!alias) {
      return prev;
    }

    return { ...prev, [alias]: value };
  }, {});
}

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
        value.map((item) => parseNested(item, docs.nested_aliases, locale)),
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
