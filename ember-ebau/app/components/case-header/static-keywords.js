import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task, timeout } from "ember-concurrency";
import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class CaseHeaderStaticKeywordsComponent extends Component {
  @service store;
  @service ebauModules;
  @service intl;
  @service notification;

  @tracked search = "";
  @tracked page = 1;

  get selected() {
    return this.args.instance.staticKeywords;
  }

  get lastKeywordId() {
    return this.staticKeywords.records?.[
      this.staticKeywords.records?.length - 1
    ]?.id;
  }

  @action
  onChange(selected) {
    this.args.instance.staticKeywords = selected;
    this.args.instance.save();
  }

  staticKeywords = paginatedQuery(this, "static-keyword", () => ({
    is_archived: false,
    page: {
      size: 10,
      number: this.page,
    },
  }));

  // We cant pass the search into the `paginatedQuery` call because
  // ember-powerselect doesn't call @search when the input is empty.
  // This will cause an empty search + empty list as in this case
  // eps will display the @options as per documentation.
  updateSearch = task({ restartable: true }, async (term) => {
    await timeout(500);
    this.page = 1;
    return await this.store.query("static-keyword", {
      is_archived: false,
      search: term,
      page: {
        // Hardcoding this as there is no nice reactive way of updating
        // the page here as eps expects the @search to return the search
        // result instead of just triggering the search.
        size: 100,
        number: 1,
      },
    });
  });

  @action
  nextPage() {
    this.page++;
  }
}
