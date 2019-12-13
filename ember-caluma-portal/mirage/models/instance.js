import { Model, belongsTo, hasMany } from "ember-cli-mirage";

export default Model.extend({
  instanceState: belongsTo("instance-state"),
  involvedApplicants: hasMany("applicant", { inverse: "instance" })
});
