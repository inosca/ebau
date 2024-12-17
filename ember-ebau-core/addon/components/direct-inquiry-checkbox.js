import { service } from "@ember/service";
import Component from "@glimmer/component";
import { trackedFunction } from "reactiveweb/function";

export default class DirectInquiryCheckboxComponent extends Component {
  @service calumaOptions;
  @service distribution;
  @service store;

  #isSubservice = trackedFunction(this, async () => {
    await Promise.resolve();

    const serviceIds = [
      this.args.context?.inquiry?.addressedGroups, // editing a single inquiry
      this.args.context?.selectedGroups, // bulk editing multiple inquiries
    ]
      .flat()
      .filter(Boolean);

    // Marking an inquiry as direct is not allowed when bulk editing more than
    // one inquiry.
    if (serviceIds.length !== 1) {
      return false;
    }

    const service = await this.store.findRecord(
      "service",
      parseInt(serviceIds[0]),
    );

    return (
      parseInt(service.belongsTo("serviceParent").id()) ===
      parseInt(this.calumaOptions.currentGroupId)
    );
  });

  get isVisible() {
    if (this.args.disabled && this.args.field.value?.length) {
      // Needs to be visible if it's selected and readonly
      return true;
    }

    const hasPendingInquiry =
      this.distribution.navigation.value?.addressed.edges.find(
        ({ node }) => node.status === "READY",
      );

    return hasPendingInquiry && this.#isSubservice.value;
  }

  get disabled() {
    return (
      this.args.disabled ||
      // If the inquiry is already sent the checkbox must be disabled as the
      // meta property used in the backend is written on send
      this.args.context?.inquiry?.status === "READY"
    );
  }
}
