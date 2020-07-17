import { Model, belongsTo, hasMany } from "ember-cli-mirage";

export default Model.extend({
  instanceState: belongsTo("instance-state"),
  activeService: belongsTo("public-service"),
  involvedApplicants: hasMany("applicant", { inverse: "instance" }),
});
