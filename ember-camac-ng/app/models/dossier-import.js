import Model, { attr, belongsTo } from "@ember-data/model";
import { inject as service } from "@ember/service";

export default class DossierImportModel extends Model {
  @service store;

  @attr createdAt;
  @attr status;
  @attr messages;
  @attr sourceFile;
  @attr mimeType;
  @attr dossierLoaderType;

  @belongsTo user;
  @belongsTo group;
  @belongsTo location;
  @belongsTo service;

  start() {
    const adapter = this.store.adapterFor("dossier-import");
    return adapter.start(this);
  }

  confirm() {
    const adapter = this.store.adapterFor("dossier-import");
    return adapter.confirm(this);
  }

  undo() {
    const adapter = this.store.adapterFor("dossier-import");
    return adapter.undo(this);
  }

  transmit() {
    const adapter = this.store.adapterFor("dossier-import");
    return adapter.transmit(this);
  }
}
