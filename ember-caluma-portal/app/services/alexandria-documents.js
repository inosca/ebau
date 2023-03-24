import DocumentsService from "ember-alexandria/services/documents";
import { inject as service } from "@ember/service";

export default class AlexandriaDocumentsService extends DocumentsService {
  @service session
  @service intl

  async upload(category, files, context) {
    if (!category.id) {
      category =
        (await this.store.peekRecord("category", category)) ||
        await this.store.findRecord("category", category);
    }

    return await Promise.all(
      Array.from(files).map(async (file) => {
        const documentModel = this.store.createRecord("document", {
          category,
          meta: { case_id: context.instanceId },
          /*
          problem with oidc_group not being set
          createdByGroup: this.session.group.id,
          modifiedByGroup: this.session.group.id,
          */
        });
        documentModel.title = file.name;
        await documentModel.save();

        const fileModel = this.store.createRecord("file", {
          name: file.name,
          type: "original",
          document: documentModel,
          /*
          createdByGroup: this.session.group.id,
          modifiedByGroup: this.session.group.id,
          */
        });
        await fileModel.save();

        const response = await fetch(fileModel.uploadUrl, {
          method: "PUT",
          body: file,
        });

        if (!response.ok) {
          throw new Error(response.statusText, response.status);
        }

        // meta is empty otherwise
        documentModel.meta = { case_id: context.instanceId };
        return documentModel;
      })
    );
  }
}
