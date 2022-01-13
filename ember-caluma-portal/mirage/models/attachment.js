import { Model, belongsTo } from "miragejs";

export default Model.extend({
  attachmentSection: belongsTo("attachment-section"),
});
