import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask, task, timeout } from "ember-concurrency";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class GisApplyButtonComponent extends Component {
  @service intl;
  @service notification;
  @service fetch;
  @service calumaStore;

  @queryManager apollo;

  @tracked data = [];
  @tracked showModal = false;

  getData = dropTask(async () => {
    if (this.args.disabled) return;

    try {
      const params = Object.entries(this.args.params)
        .map(([key, value]) => `${key}=${value}`)
        .join("&");

      this.args.onGetData?.();

      const response = await this.fetch.fetch(`/api/v1/gis/data/?${params}`, {
        headers: { accept: "application/json" },
      });

      let data;
      let errors;
      let cache;

      if (hasFeature("gis.v3")) {
        const { task_id } = await response.json();
        ({
          data,
          cache = null,
          errors = [],
        } = await this.pollData.perform(task_id));
      } else {
        ({ data, cache, errors = [] } = await response.json());
      }

      if (errors.length) {
        errors.forEach(({ detail }) => {
          this.notification.danger(detail);
        });
      }

      this.data = data;
      this.cacheKey = cache;
      this.showModal = true;
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("gis.apply-error"));
    }
  });

  pollData = task(async (taskId) => {
    this.notification.warning(this.intl.t("gis.loadingHint"));

    let response;

    while (!response || response.status === 202) {
      /* eslint-disable no-await-in-loop */
      response = await this.fetch.fetch(`/api/v1/gis/data/${taskId}/`, {
        headers: { accept: "application/json" },
      });

      if (!response.ok) {
        throw new Error("Error while polling GIS task results.");
      }

      await timeout(1000);
      /* eslint-enable no-await-in-loop */
    }

    return await response.json();
  });

  applyData = dropTask(async () => {
    const response = await this.fetch.fetch(`/api/v1/gis/apply`, {
      method: "POST",
      body: JSON.stringify({
        cache: this.cacheKey,
        instance: this.args.instanceId,
      }),
      headers: {
        "content-type": "application/json",
        accept: "application/json",
      },
    });

    const { questions } = await response.json();

    this.showModal = false;

    await Promise.all(
      questions.map((slug) =>
        this.args.document.findField(slug)?.refreshAnswer.linked().perform(),
      ),
    );
  });
}
