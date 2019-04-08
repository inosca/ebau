import Route from "@ember/routing/route";

export default Route.extend({
  model({ case_id }) {
    console.log("model", case_id);
    return case_id;
  }
});
