import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { task, restartableTask, timeout } from "ember-concurrency";
import { confirm } from "ember-uikit";

import paginatedQuery from "ember-ebau-core/resources/paginated";
import parseError from "ember-ebau-core/utils/parse-error";

export default class ServicePermissionsStaticKeywordsController extends Controller {
  @service store;
  @service intl;
  @service session;
  @service notification;

  @tracked page = 1;
  @tracked staticKeywordName;
  @tracked search = "";

  @action
  updatePage() {
    if (this.staticKeywords.hasMore && !this.staticKeywords.isLoading) {
      this.page += 1;
    }
  }

  staticKeywords = paginatedQuery(this, "static-keyword", () => ({
    search: this.search,
    page: {
      number: this.page,
      size: 20,
    },
  }));

  updateSearch = restartableTask(async (event) => {
    await timeout(500);

    this.search = event.target.value;
    this.page = 1;
  });

  save = task({ drop: true }, async (event) => {
    event.preventDefault();

    // Check if the keyword already exists in the store
    const existingKeyword = await this.store.query("static-keyword", {
      name: this.staticKeywordName,
      service: this.session.service.id,
    });

    if (existingKeyword.toArray().length > 0) {
      this.notification.danger(
        this.intl.t("service-permissions.static-keywords-already-exists"),
      );
      return;
    }

    const staticKeyword = this.store.createRecord("static-keyword", {
      name: this.staticKeywordName,
      service: this.session.service,
    });

    try {
      await staticKeyword.save();
      this.page = 1;
      this.staticKeywordName = "";
      this.search = "";

      this.notification.success(
        this.intl.t("service-permissions.static-keywords-save-success"),
      );
    } catch (error) {
      this.notification.danger(
        parseError(error, false) ??
          this.intl.t("service-permissions.static-keywords-save-error"),
      );

      staticKeyword.rollbackAttributes();
    }
  });

  delete = task({ drop: true }, async (staticKeyword, event) => {
    event.preventDefault();

    if (
      await confirm(
        this.intl.t("service-permissions.static-keywords-delete-confirm"),
        {
          i18n: {
            ok: this.intl.t("global.delete"),
          },
        },
      )
    ) {
      await staticKeyword.destroyRecord();
    }
  });
}
