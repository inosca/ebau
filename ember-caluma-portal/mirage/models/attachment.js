import { Model, belongsTo } from "ember-cli-mirage";

export default Model.extend({
  attachmentSection: belongsTo("attachment-section"),
});
