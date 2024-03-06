import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { query } from "ember-data-resources";
import municipalityQuery from "ember-ebau-core/gql/queries/municipality.graphql";
import apolloQuery from "ember-ebau-core/resources/apollo";
import parseError from "ember-ebau-core/utils/parse-error";

export default class InstancesEditApplicantsController extends Controller {
  @service intl;
  @service notification;
  @service store;
  @service fetch;

  @controller("instances.edit") editController;

  @tracked email = "";

  municipalityPermissions = query(this, "instance-acl", () => ({
    access_level: "municipality-before-submission",
    include: "service,created_by_user,revoked_by_user",
    instance: this.editController.model,
  }));

  get municipalityHasPermission() {
    return (
      this.municipalityPermissions.records?.some(
        (acl) => acl.status === "active",
      ) ?? false
    );
  }

  currentMunicipality = apolloQuery(
    this,
    () => ({
      query: municipalityQuery,
      fetchPolicy: "network-only",
      variables: { instanceId: this.editController.model },
    }),
    "allCases.edges",
    (data) => {
      return data[0].node.document.answers.edges[0]?.node.value;
    },
  );

  get applicants() {
    return this.editController.instance?.involvedApplicants;
  }

  get usedEmails() {
    return this.applicants?.map((applicant) => applicant.email);
  }

  @dropTask
  *add(event) {
    event.preventDefault();

    const user = this.store.createRecord("applicant", {
      email: this.email,
      instance: this.editController.instance,
    });

    try {
      yield user.save({ adapterOptions: { include: "invitee,user" } });

      this.email = "";

      this.notification.success(this.intl.t("instances.applicants.addSuccess"));
    } catch (error) {
      // eslint-ignore-next-line no-console
      console.error(error);
      yield user.destroyRecord();
      this.notification.danger(
        parseError(error) || this.intl.t("instances.applicants.addError"),
      );
    }
  }

  @dropTask
  *delete(applicant) {
    if (this.applicants.length < 2) return;

    try {
      yield applicant.destroyRecord();

      this.notification.success(
        this.intl.t("instances.applicants.deleteSuccess"),
      );
    } catch (error) {
      // eslint-ignore-next-line no-console
      console.error(error);
      this.notification.danger(
        parseError(error) || this.intl.t("instances.applicants.deleteError"),
      );
    }
  }

  @dropTask
  *toggleMunicipalityAccess() {
    try {
      yield this.fetch.fetch(
        `/api/v1/instances/${this.editController.model}/grant-municipality-access`,
        { method: this.municipalityHasPermission ? "DELETE" : "POST" },
      );

      yield this.municipalityPermissions.retry();
    } catch (error) {
      // eslint-ignore-next-line no-console
      console.error(error);
      this.notification.danger(parseError(error));
    }
  }
}
