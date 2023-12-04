import { inject as service } from "@ember/service";
import { macroCondition, isTesting } from "@embroider/macros";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { task, timeout } from "ember-concurrency";
import mainConfig from "ember-ebau-core/config/main";
import { trackedFunction } from "ember-resources/util/function";
import { dedupeTracked } from "tracked-toolbox";

const { answerSlugs } = mainConfig;

export default class ActiveMunicipalityLogoComponent extends Component {
  @service store;
  @service calumaStore;

  @dedupeTracked serviceId;

  constructor(...args) {
    super(...args);

    this.pollService.perform();
  }

  @task
  *pollService() {
    while (true) {
      const documentId = decodeId(this.args.case.document.id);
      const document = this.calumaStore.find(`Document:${documentId}`);
      const answer = document?.findAnswer(answerSlugs.municipality);

      this.serviceId = answer ?? this.args.case.municipalityId ?? null;

      if (macroCondition(isTesting())) {
        // do not poll in testing
        return;
      }

      yield timeout(document ? 1000 : 5000);
    }
  }

  service = trackedFunction(this, async () => {
    if (!this.serviceId) return null;

    await Promise.resolve();

    return (
      this.store.peekRecord("public-service", this.serviceId) ??
      (await this.store.findRecord("public-service", this.serviceId))
    );
  });
}
