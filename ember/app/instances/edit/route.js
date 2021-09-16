import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import SessionStorageStore from "ember-simple-auth/session-stores/session-storage";
import { all } from "rsvp";

export default class InstancesEditRoute extends Route {
  @service ajax;
  @service questionStore;
  @service session;

  queryParams = {
    group: { refreshModel: true },
    publication: {},
  };

  async model({ instance_id: id, group, publication = false }) {
    this.viewedByPublication = publication;
    this.session.set("data.enforcePublicAccess", this.viewedByPublication);

    const response = await this.ajax.request(`/api/v1/instances/${id}`, {
      data: {
        group,
        include: "form,instance_state,location",
      },
      headers: {
        Accept: "application/vnd.api+json",
        ...(this.viewedByPublication ? { "x-camac-public-access": true } : {}),
      },
    });

    await this.store.query("form-field", { instance: id, group });
    await this.store.query("attachment", {
      instance: id,
      group,
      include: "attachment-sections",
    });

    const {
      data: { meta },
    } = response;

    this.store.pushPayload(response);

    return {
      instance: this.store.peekRecord("instance", id),
      meta,
    };
  }

  async afterModel(model) {
    const { forms, modules } = await this.questionStore.config;

    const questions = [
      ...new Set(
        forms[model.instance.get("form.name")].reduce((qs, mod) => {
          return [...qs, ...modules[mod].questions];
        }, [])
      ),
    ];

    const build = (name) =>
      this.questionStore.buildQuestion(name, model.instance.id);

    const questionObjects = await all(questions.map(await build));

    this.questionStore._store.pushObjects(questionObjects);
  }

  async setupController(controller, model) {
    super.setupController(controller, model);

    controller.instanceTransformation.perform();

    if (this.viewedByPublication) {
      const session = SessionStorageStore.create({ _isFastBoot: false });
      const storage = await session.restore();

      if (!("publicationsSeen" in storage)) {
        storage.publicationsSeen = [];
      }

      if (!storage.publicationsSeen.includes(this.viewedByPublication)) {
        this.ajax.request(
          `/api/v1/publication-entries/${this.viewedByPublication}/viewed`,
          {
            method: "POST",
            headers: {
              Accept: "application/vnd.api+json",
            },
          }
        );
        storage.publicationsSeen.push(this.viewedByPublication);
      }

      await session.persist(storage);
    }
  }

  resetController(_, isExiting) {
    if (isExiting) {
      // We clear the store and the question store at this point so we do not
      // have too much unnecessary data in the memory
      this.store.unloadAll();
      this.questionStore.clear();
      this.session.set("data.enforcePublicAccess", false);
    }
  }
}
