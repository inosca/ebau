import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import {
  dropTask,
  lastValue,
  restartableTask,
  timeout,
} from "ember-concurrency";
import mainConfig from "ember-ebau-core/config/main";
import fetch from "fetch";

export default class DossierImportIndexController extends Controller {
  @service intl;
  @service notification;
  @service store;
  @service shoebox;
  @service session;

  @tracked fileUpload;
  @tracked selectedLocation;
  @tracked selectedGroup;

  @lastValue("fetchGroups") groups;
  @restartableTask
  *fetchGroups() {
    if (!mainConfig.useLocation && this.shoebox.isSupportRole) {
      return yield this.store.query("group", {
        role: this.shoebox.content.config.roles["municipality-admin"][0],
        service_group: 2,
        include: "service",
      });
    }
    const group = yield this.store.findRecord(
      "group",
      this.shoebox.content.groupId,
    );
    return [group];
  }

  @lastValue("fetchLocations") locations;
  @restartableTask
  *fetchLocations() {
    if (!mainConfig.useLocation) {
      return [];
    }
    if (this.shoebox.isSupportRole) {
      return yield this.store.findAll("location");
    }
    const group = yield this.store.findRecord(
      "group",
      this.shoebox.content.groupId,
    );
    return group.locations;
  }

  @dropTask
  *upload(event) {
    this.notification.clear();

    // Prevent uikit's uk-upload from removing files
    // from underlying input field
    event.stopPropagation();

    const formData = new FormData();
    formData.append(
      "group",
      this.selectedGroup?.id || this.groups.firstObject?.id,
    );

    if (mainConfig.useLocation) {
      formData.append(
        "location_id",
        this.selectedLocation?.id || this.locations.firstObject?.id,
      );
    }

    // Only one zip file is allowed by dropzone and input link
    const files = event.detail?.[0] ?? event.target.files;
    const file = files?.[0];
    if (file.size > mainConfig.maxDossierImportSize) {
      // Force component template to reload
      yield timeout(200);
      this.notification.danger(
        this.intl.t("dossierImport.new.uploadError.fileTooLarge"),
      );
      return (this.fileUpload = {
        id: null,
        file,
      });
    }
    formData.append("source_file", file);

    // Don't use fetch service to preserve headers'
    // content-type boundary value
    const response = yield fetch(`/api/v1/dossier-imports`, {
      method: "POST",
      headers: {
        authorization: yield this.session.getAuthorizationHeader(),
        "accept-language": this.shoebox.content.language,
        "x-camac-group": this.shoebox.content.groupId,
      },
      body: formData,
    });

    if (!response.ok) {
      yield this.handleUploadError(response);
      this.fileUpload = { id: null, file };
      return this.fileUpload;
    }

    const id = (yield response.json()).data.id;
    this.fileUpload = { id, file };
    return this.fileUpload;
  }

  async handleUploadError(response) {
    if (response.status === 413) {
      this.notification.danger(
        this.intl.t(`dossierImport.new.uploadError.fileTooLarge`),
      );
      return;
    }
    const message = (await response.json()).errors[0].detail;
    this.notification.danger(message);
  }

  @action
  updateLocation(location) {
    this.selectedLocation = location;
  }

  @action
  updateGroup(group) {
    this.selectedGroup = group;
  }

  @action
  clearNotifications() {
    this.notification.clear();
  }
}
