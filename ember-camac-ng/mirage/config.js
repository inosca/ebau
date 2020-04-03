/* eslint-disable ember/no-get */
export default function() {
  // this.urlPrefix = "";
  // this.namespace = "";
  this.timing = 1000;

  this.get("/api/v1/services");
  this.get("/api/v1/services/:id");
  this.patch("/api/v1/services/:id");

  this.passthrough("/index/token");
}
