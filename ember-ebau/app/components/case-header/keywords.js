import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { findAll } from "ember-data-resources";

export default class CaseHeaderKeywordsComponent extends Component {
  @service store;
  @service ebauModules;
  @service intl;
  @service notification;

  allAvailable = findAll(this, "keyword");

  get available() {
    return this.allAvailable.records?.filter(
      ({ id }) => !this.selected.map((kw) => kw.id).includes(id),
    );
  }

  get selected() {
    return this.args.instance.keywords;
  }

  @action
  onChange(selected) {
    this.args.instance.keywords = selected;
    this.args.instance.save();
  }

  // this action only overwrites the built-in text "add" from ember-power-select-with-create
  @action
  customSuggestion(term) {
    return this.intl.t("cases.header.addKeyword", { term });
  }

  @dropTask
  *create(name) {
    const service = yield this.store.peekRecord(
      "service",
      this.ebauModules.serviceId,
    );
    let keyword = this.available.find((kw) => kw.name === name);
    try {
      if (!keyword) {
        keyword = yield this.store.createRecord("keyword", {
          name,
          service,
          instances: [this.args.instance],
        });
        yield keyword.save();
      } else {
        const keywords = yield this.args.instance.keywords;
        keywords.push(keyword);
        this.args.instance.save();
      }
    } catch (e) {
      this.notification.danger(this.intl.t("cases.header.keywordSaveFailed"));
      console.error(e);
      const keywords = yield this.args.instance.keywords;
      keywords.pop(keyword);
    }
  }
}
