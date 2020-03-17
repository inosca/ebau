import Route from "@ember/routing/route";

export default class InstancesEditIndexRoute extends Route {
  model() {
    return this.modelFor("instances.edit");
  }
}

// import Route from "@ember/routing/route";
// import { next } from "@ember/runloop";

// export default Route.extend({
//   redirect() {
//     next(async () => {
//       const controller = this.controllerFor("instances.edit");
//       const instance = await controller.instanceTask.last;

//       if (instance && instance.mainForm) {
//         this.replaceWith("instances.edit.form", instance.mainForm.slug);
//       }
//     });
//   }
// });
