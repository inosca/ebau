import { inject as service } from "@ember/service";
import Model, { attr, belongsTo } from "@ember-data/model";

export default class DossierImportModel extends Model {
  @service store;

  @attr createdAt;
  @attr status;
  @attr messages;
  @attr sourceFile;
  @attr filename;
  @attr mimeType;
  @attr dossierLoaderType;

  @belongsTo("user", { inverse: null, async: true }) user;
  @belongsTo("group", { inverse: null, async: true }) group;
  @belongsTo("location", { inverse: null, async: true }) location;
  @belongsTo("service", { inverse: null, async: true }) service;

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

  clean() {
    const adapter = this.store.adapterFor("dossier-import");
    return adapter.clean(this);
  }

  transmit() {
    const adapter = this.store.adapterFor("dossier-import");
    return adapter.transmit(this);
  }
}
