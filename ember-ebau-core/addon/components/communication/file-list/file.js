import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class CommunicationFileListFileComponent extends Component {
  @service router;
  @service ebauModules;

  get instanceId() {
    return this.router.currentRoute.parent.params.instance_id;
  }

  get messageByApplicant() {
    return this.args.file.get("message.createdBy.id") === "APPLICANT";
  }
}
