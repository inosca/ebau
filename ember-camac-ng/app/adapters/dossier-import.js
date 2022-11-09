import ApplicationAdapter from "camac-ng/adapters/application";

export default class DossierImportAdapter extends ApplicationAdapter {
  start(model) {
    const url = `${this.buildURL("dossier-import", model.id)}/start`;
    return this.ajax(url, "POST");
  }

  confirm(model) {
    const url = `${this.buildURL("dossier-import", model.id)}/confirm`;
    return this.ajax(url, "POST");
  }

  undo(model) {
    const url = `${this.buildURL("dossier-import", model.id)}/undo`;
    return this.ajax(url, "POST");
  }

  transmit(model) {
    const url = `${this.buildURL("dossier-import", model.id)}/transmit`;
    return this.ajax(url, "POST");
  }
}
