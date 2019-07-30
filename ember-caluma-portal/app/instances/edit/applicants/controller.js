import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { reads } from "@ember/object/computed";
import { task } from "ember-concurrency";
import QueryParams from "ember-parachute";

const queryParams = new QueryParams({});

const findUser = (data, id) =>
  data.find(obj => obj.type === "users" && parseInt(obj.id) === parseInt(id));

const parse = obj => ({ ...obj.attributes, id: parseInt(obj.id) });

class User {
  constructor(raw) {
    Object.assign(this, raw);
  }

  get fullName() {
    return `${this.name} ${this.surname}`;
  }
}

export default Controller.extend(queryParams.Mixin, {
  fetch: service(),
  intl: service(),
  notification: service(),

  editController: controller("instances.edit"),
  instanceId: reads("editController.model"),

  setup() {
    this.applicantsTask.perform();
  },

  reset() {
    this.applicantsTask.cancelAll({ reset: true });
  },

  applicants: reads("applicantsTask.lastSuccessful.value"),
  applicantsTask: task(function*() {
    const response = yield this.fetch.fetch(
      `/api/v1/applicants?instance=${this.instanceId}&include=invitee,user`
    );
    const { data, included } = yield response.json();

    return data.map(obj => {
      const user = findUser(included, obj.relationships.user.data.id);
      const invitee = findUser(included, obj.relationships.invitee.data.id);

      return {
        ...parse(obj),
        user: new User(parse(user)),
        invitee: new User(parse(invitee))
      };
    });
  }).drop(),

  add: task(function*(event) {
    event.preventDefault();

    const email = event.srcElement.querySelector("input[name=email]").value;

    try {
      const response = yield this.fetch.fetch("/api/v1/applicants", {
        method: "post",
        body: JSON.stringify({
          data: {
            type: "applicants",
            attributes: { email },
            relationships: {
              instance: {
                data: {
                  id: this.instanceId,
                  type: "instances"
                }
              }
            }
          }
        })
      });

      if (!response.ok) {
        const { errors } = yield response.json();

        if (
          errors.some(({ detail }) => /User.*could not be found/.test(detail))
        ) {
          this.notification.danger(
            this.intl.t("instances.applicants.addDoesNotExist", { email })
          );

          return;
        }

        if (
          errors.some(({ detail }) => /User.*already has access/.test(detail))
        ) {
          this.notification.danger(
            this.intl.t("instances.applicants.addHasAccess", { email })
          );

          return;
        }

        throw new Error();
      }

      yield this.applicantsTask.perform();

      event.srcElement.querySelector("input[name=email]").value = "";

      this.notification.success(this.intl.t("instances.applicants.addSuccess"));
    } catch (error) {
      // eslint-ignore-next-line no-console
      console.error(error);
      this.notification.danger(this.intl.t("instances.applicants.addError"));
    }
  }).drop(),

  delete: task(function*(applicant) {
    if (this.applicants.length < 2) return;

    try {
      yield this.fetch.fetch(`/api/v1/applicants/${applicant.id}`, {
        method: "delete"
      });

      yield this.applicantsTask.perform();

      this.notification.success(
        this.intl.t("instances.applicants.deleteSuccess")
      );
    } catch (error) {
      // eslint-ignore-next-line no-console
      console.error(error);
      this.notification.danger(this.intl.t("instances.applicants.deleteError"));
    }
  }).drop()
});
