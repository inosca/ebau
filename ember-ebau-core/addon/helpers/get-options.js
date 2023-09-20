import Helper from "@ember/component/helper";

export default class GetOptions extends Helper {
  _lastValue = [];

  compute([obj, key]) {
    const result = obj[key];

    if (result?.isPending) {
      return this._lastValue;
    }

    const value = result?.records ?? result?.value ?? result ?? [];

    this._lastValue = value;

    return value;
  }
}
