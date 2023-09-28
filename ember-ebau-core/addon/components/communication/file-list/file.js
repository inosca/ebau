import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class CommunicationFileListFileComponent extends Component {
  @service router;
  @service ebauModules;
  @service intl;
}
