import ApplicationAdapter from "camac-ng/adapters/application";

export default class CamacTagAdapter extends ApplicationAdapter {
  pathForType() {
    return "tags";
  }
}
