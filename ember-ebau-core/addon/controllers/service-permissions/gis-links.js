import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { task, restartableTask, timeout } from "ember-concurrency";
import { confirm } from "ember-uikit";

import paginatedQuery from "ember-ebau-core/resources/paginated";
import parseError from "ember-ebau-core/utils/parse-error";

export default class ServicePermissionsGisLinksController extends Controller {
  pageSize = 50;

  @service store;
  @service intl;
  @service session;
  @service notification;

  @tracked offset = 0;
  @tracked gisLinkName;
  @tracked gisLinkPlaceholder;
  @tracked search = "";

  @action
  updatePage() {
    if (this.gisLinks.hasMore && !this.gisLinks.isLoading) {
      this.offset += this.pageSize;
    }
  }

  gisLinks = paginatedQuery(this, "gis-link", () => ({
    ...(this.search ? { "filter[name]": { ilike: `%${this.search}%` } } : {}),
    page: {
      offset: this.offset,
      limit: this.pageSize,
      count: true,
    },
  }));

  updateSearch = restartableTask(async (event) => {
    await timeout(500);

    this.search = event.target.value;
    this.offset = 0;
  });

  save = task({ drop: true }, async (event) => {
    event.preventDefault();

    const gisLink = this.store.createRecord("gis-link", {
      name: this.gisLinkName,
      placeholder: this.gisLinkPlaceholder,
      service: this.session.service,
    });

    try {
      await gisLink.save();
      this.offset = 0;
      this.gisLinkName = "";
      this.gisLinkPlaceholder = "";
      this.search = "";

      this.notification.success(
        this.intl.t("service-permissions.gis-links-save-success"),
      );
    } catch (error) {
      this.notification.danger(
        parseError(error, false) ??
          this.intl.t("service-permissions.gis-links-save-error"),
      );

      gisLink.rollbackAttributes();
    }
  });

  delete = task({ drop: true }, async (gisLink, event) => {
    event.preventDefault();

    if (
      await confirm(
        this.intl.t("service-permissions.gis-links-delete-confirm"),
        {
          i18n: {
            ok: this.intl.t("global.delete"),
          },
        },
      )
    ) {
      await gisLink.destroyRecord();
    }
  });
}
