import Component from "@ember/component";
import { computed } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import download from "downloadjs";
import Ember from "ember";
import { task } from "ember-concurrency";
import fetch from "fetch";

export default Component.extend({
  session: service(),
  notification: service(),

  token: reads("session.data.authenticated.access_token"),

  headers: computed("token", function () {
    return {
      Authorization: `Bearer ${this.token}`,
    };
  }),

  tagName: "button",

  classNames: ["uk-button", "uk-button-large", "uk-button-primary"],

  click() {
    this.download.perform();
  },

  download: task(function* () {
    try {
      const url = `/api/v1/instances/${
        this.instance.id
      }/export_detail?type=pdf${this.group ? `&group=${this.group}` : ""}
      `;

      const response = yield fetch(url, {
        mode: "cors",
        headers: this.headers,
      });

      const file = yield response.blob();

      if (!Ember.testing) {
        download(
          file,
          `${this.get("instance.form.description")}.pdf`,
          file.type
        );
      }

      this.notification.success("Datei wurde erfolgreich heruntergeladen");
    } catch (e) {
      this.notification.danger(
        "Hoppla, beim Herunterladen der Datei ist etwas schief gelaufen. Bitte versuchen Sie es nochmals"
      );
    }
  }).drop(),
});
