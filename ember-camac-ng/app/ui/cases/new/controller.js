import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allForms } from "@projectcaluma/ember-core/caluma-query/queries";
import {
  restartableTask,
  dropTask,
  lastValue,
} from "ember-concurrency-decorators";

import ENV from "camac-ng/config/environment";

export default class CasesNewController extends Controller {
  @service fetch;
  @service shoebox;

  @tracked selectedForm = null;

  @calumaQuery({ query: allForms })
  formQuery;

  @lastValue("fetchForms") forms;
  @restartableTask
  *fetchForms() {
    yield this.formQuery.fetch({
      filter: [
        { isPublished: true },
        { isArchived: false },
        { orderBy: "NAME_ASC" },
        // exclude public forms, only include creatable forms
        {
          metaValue: [{ key: "visibility", value: { type: "public" } }],
          invert: true,
        },
        {
          metaValue: [{ key: "is_creatable", value: true }],
        },
      ],
    });
  }

  @dropTask
  *createCase() {
    const body = {
      data: {
        attributes: {
          "caluma-form": this.selectedForm,
        },
        type: "instances",
      },
    };

    if (ENV.APPLICATION?.newCase.calumaWorkflow) {
      body.data.attributes["caluma-workflow"] =
        ENV.APPLICATION.newCase.calumaWorkflow;
    }
    if (ENV.APPLICATION?.newCase.camacForm) {
      body.data.relationships = {
        form: {
          data: {
            id: ENV.APPLICATION.newCase.camacForm,
            type: "forms",
          },
        },
      };
    }

    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify(body),
    });

    const {
      data: { id: instanceId },
    } = yield response.json();

    location.assign(
      `/index/redirect-to-instance-resource/instance-id/${instanceId}/`
    );
  }
}
