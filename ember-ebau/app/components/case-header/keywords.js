import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { task, timeout } from "ember-concurrency";

export default class CaseHeaderKeywordsComponent extends Component {
  @service store;
  @service ebauModules;
  @service intl;
  @service notification;

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

  search = task({ restartable: true }, async (term) => {
    await timeout(300);
    return await this.store.query("keyword", {
      search: term,
      exclude_instance: this.args.instance.id,
      page: {
        limit: 10,
      },
    });
  });

  create = task({ drop: true }, async (name) => {
    const service = this.store.peekRecord(
      "service",
      this.ebauModules.serviceId,
    );
    let keyword = this.store.peekAll("keyword").find((kw) => kw.name === name);

    try {
      if (!keyword) {
        keyword = await this.store.createRecord("keyword", {
          name,
          service,
          instances: [this.args.instance],
        });
        await keyword.save();
      } else {
        const keywords = await this.args.instance.keywords;
        keywords.push(keyword);
        this.args.instance.save();
      }
    } catch (e) {
      this.notification.danger(this.intl.t("cases.header.keywordSaveFailed"));
      console.error(e);
      const keywords = await this.args.instance.keywords;
      keywords.pop(keyword);
    }
  });
}
