import config from "../config/environment";
import { Response } from "ember-cli-mirage";

const { tokenEndpoint, logoutEndpoint } = config["ember-simple-auth-oidc"];

export default function() {
  this.urlPrefix = ""; // make this `http://localhost:8080`, for example, if your API is on a different server
  this.namespace = ""; // make this `/api`, for example, if your API is namespaced
  this.timing = 400; // delay for each request, automatically set to 0 during testing
  this.logging = false;

  this.passthrough("https://map.geo.sz.ch/**");

  this.post(tokenEndpoint, () => {
    let tokenBody = btoa(
      JSON.stringify({
        exp: Math.round(new Date().getTime() + (30 * 60 * 1000) / 1000)
      })
    );

    return {
      access_token: `access.${tokenBody}.token`,
      refresh_token: `refresh.${tokenBody}.token`
    };
  });

  this.post(logoutEndpoint, () => {});

  this.get("/api/v1/form-config", { forms: {}, modules: {}, questions: {} });

  this.get("/api/v1/forms");

  this.get("/api/v1/instances");
  this.post("/api/v1/instances");
  this.get("/api/v1/instances/:id");
  this.patch("/api/v1/instances/:id");
  this.delete("/api/v1/instances/:id");
  this.post("/api/v1/instances/:id/submit", () => new Response(200));

  this.get("/api/v1/form-fields", function(
    { formFields },
    { queryParams: { instance, name } }
  ) {
    return formFields.where(field => {
      return (
        (name ? name.split(",").includes(field.name) : true) &&
        (instance ? field.instanceId === instance : true)
      );
    });
  });

  this.post("/api/v1/form-fields");
  this.get("/api/v1/form-fields/:id");
  this.patch("/api/v1/form-fields/:id");

  this.get("/api/v1/attachments", function(
    { attachments },
    { queryParams: { instance, name } }
  ) {
    return attachments.where(field => {
      return (
        (name
          ? name.split(",").some(n => new RegExp(n).test(field.name))
          : true) && (instance ? field.instanceId === instance : true)
      );
    });
  });

  this.post("/api/v1/attachments");
  this.get("/api/v1/attachments/:id");
  this.get("/api/v1/attachments/:id/thumbnail", () => new Blob());
  this.patch("/api/v1/attachments/:id");
}
