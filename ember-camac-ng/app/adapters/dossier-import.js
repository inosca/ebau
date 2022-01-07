import ApplicationAdapter from "./application";

export default class DossierImportAdapter extends ApplicationAdapter {
  start(model) {
    const url = `${this.buildURL("dossier-import", model.id)}/start`;
    return this.ajax(url, "POST");
  }
}
