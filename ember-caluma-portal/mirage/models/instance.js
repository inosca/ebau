import { Model, belongsTo, hasMany } from "miragejs";

export default Model.extend({
  instanceState: belongsTo("instance-state"),
  activeService: belongsTo("public-service"),
  involvedApplicants: hasMany("applicant", { inverse: "instance" }),
});
