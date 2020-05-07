import Controller from "@ember/controller";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import ENV from "citizen-portal/config/environment";
import { task } from "ember-concurrency";

export default Controller.extend({
  questionStore: service(),
  ajax: service(),
  notification: service(),
  store: service(),

  parcels: computed("model.instance.id", function() {
    return this.questionStore.peek("parzellen", this.model.instance.id);
  }),

  points: computed("model.instance.id", function() {
    return this.questionStore.peek("punkte", this.model.instance.id);
  }),

  layers: computed("model.instance.id", function() {
    return this.questionStore.peek("layer", this.model.instance.id);
  }),

  attachment: computed("model.instance.id", function() {
    return this.questionStore.peek(
      "dokument-grundstucksangaben",
      this.model.instance.id
    );
  }),

  specialForm: computed("model.instance.form.id", function() {
    return ENV.APP.formLocations[this.get("model.instance.form.id")];
  }),

  _saveImage: task(function*(image) {
    const attachment = this.attachment;
    const filename = `${attachment.get("name")}.${image.type.split("/").pop()}`;
    const formData = new FormData();

    // Delete all previous images
    this.store
      .peekAll("attachment")
      .filterBy("name", filename)
      .forEach(image => image.destroyRecord());

    formData.append("instance", attachment.get("instanceId"));
    formData.append("question", attachment.get("name"));
    formData.append(
      "attachment_sections",
      ENV.APP.attachmentSections.applicant
    );
    formData.append("path", image, filename);

    const response = yield this.ajax.request("/api/v1/attachments", {
      method: "POST",
      cache: false,
      contentType: false,
      processData: false,
      data: formData,
      headers: {
        Accept: "application/vnd.api+json"
      }
    });

    this.store.pushPayload(response);

    attachment.set(
      "model",
      this.questionStore._getModelForAttachment(
        attachment.get("name"),
        attachment.get("instanceId")
      )
    );
  }),

  _saveParcels: task(function*(parcels) {
    this.set(
      "parcels.model.value",
      parcels.map(({ number, ...p }) => ({
        ...p,
        number: parseInt(number),
        coordinates: undefined
      }))
    );

    yield this.get("questionStore.saveQuestion").perform(this.parcels);
  }),

  _savePoints: task(function*(points) {
    this.set(
      "points.model.value",
      points.map(pointSet =>
        pointSet.map(point => ({ ...point, layers: undefined }))
      )
    );

    yield this.get("questionStore.saveQuestion").perform(this.points);
  }),

  _saveLocation: task(function*(name) {
    const instance = this.get("model.instance");

    name = this.specialForm || name;

    const location = yield this.store.query("location", {
      name
    });

    instance.set("location", location.get("firstObject"));

    yield instance.save();
  }),

  _saveLayers: task(function*(affectedLayers) {
    this.set(
      "layers.model.value",
      affectedLayers.map(layer => ({ name: layer }))
    );

    yield this.get("questionStore.saveQuestion").perform(this.layers);
  }),

  saveLocation: task(function*(
    parcels,
    points,
    image,
    municipality,
    affectedLayers
  ) {
    if (this.get("model.instance.identifier")) {
      return;
    }

    try {
      yield this._saveLocation.perform(municipality);
      yield this._saveImage.perform(image);

      yield this._saveParcels.perform(parcels);
      yield this._savePoints.perform(points);
      yield this._saveLayers.perform(affectedLayers);

      this.notification.success("Ihre Auswahl wurde erfolgreich gespeichert", {
        status: "success"
      });
    } catch (e) {
      this.notification.danger(
        "Hoppla, etwas ist schief gelaufen. Bitte versuchen Sie es erneut."
      );
    }
  })
});
