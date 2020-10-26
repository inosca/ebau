/* eslint-disable ember/no-get */
export default function () {
  // this.urlPrefix = "";
  // this.namespace = "";
  this.timing = 1000;

  this.get("/api/v1/instances/:id");

  this.get("/api/v1/services");
  this.get("/api/v1/services/:id");
  this.patch("/api/v1/services/:id");

  this.get("/api/v1/history-entries");

  this.get("/api/v1/journal-entries");
  this.post("/api/v1/journal-entries");
  this.patch("/api/v1/journal-entries/:id");

  this.passthrough("/index/token");
}
