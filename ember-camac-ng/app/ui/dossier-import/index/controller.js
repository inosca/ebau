import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import dateTime from "camac-ng/utils/date-time";

export default class DossierImportIndexController extends Controller {
  @service intl;
  @service notifications;
  @service store;
  @service shoebox;
  @service session;
  @service fetch;

  @lastValue("fetchImports") imports;
  @dropTask
  *fetchImports() {
    const response = yield this.fetch.fetch(
      `/api/v1/dossier-imports?${new URLSearchParams({
        "page[size]": 10,
        include: "user",
      })}`,
      {
        method: "GET",
      }
    );

    if (!response.ok) {
      this.notifications.error(
        this.intl.t("dossierImport.imports.fetchImportsError")
      );
      return;
    }

    const json = yield response.json();
    const imports = json.data;
    return imports.map((data) => {
      const user = json.included.find(
        (user) => user.id === data.relationships.user.data.id
      ).attributes;
      const createDate = new Date(data.attributes["created-at"]);
      return {
        id: data.id,
        data: {
          createDate: dateTime(createDate),
          author: `${user.name} ${user.surname}`,
          status: this.intl.t(
            `dossierImport.imports.status.${data.attributes.status}`
          ),
          importDate: null, // TODO implement as soon as imports are possible
        },
      };
    });
  }

  @action
  clearNotifications() {
    this.notifications.clear();
  }
}
