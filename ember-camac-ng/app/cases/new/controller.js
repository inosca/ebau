import Controller from "@ember/controller";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allForms } from "@projectcaluma/ember-core/caluma-query/queries";
import { restartableTask, dropTask, lastValue } from "ember-concurrency";
import mainConfig from "ember-ebau-core/config/main";

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
      order: [{ attribute: "NAME", direction: "ASC" }],
      filter: [
        { isPublished: true },
        { isArchived: false },
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

    if (mainConfig.newCase?.calumaWorkflow) {
      body.data.attributes["caluma-workflow"] =
        mainConfig.newCase?.calumaWorkflow;
    }
    if (mainConfig.newCase?.camacForm) {
      body.data.relationships = {
        form: {
          data: {
            id: mainConfig.newCase.camacForm,
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
      `/index/redirect-to-instance-resource/instance-id/${instanceId}/`,
    );
  }
}
