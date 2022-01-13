import QueryParams from "ember-parachute";
import moment from "moment";

import config from "caluma-portal/config/environment";

const DATE_URL_FORMAT = "YYYY-MM-DD";

const dateQueryParam = {
  serialize(value) {
    const date = moment.utc(value);

    return date.isValid()
      ? date.utc().format(DATE_URL_FORMAT)
      : this.defaultValue;
  },
  deserialize(value) {
    const date = moment.utc(value, DATE_URL_FORMAT);

    return date.isValid() ? date.toDate() : this.defaultValue;
  },
};

export const queryParams = new QueryParams({
  types: {
    defaultValue: [],
    replace: true,
    serialize(value) {
      return value.toString();
    },
    deserialize(value) {
      if (!value) {
        return [];
      }
      return value.split(",");
    },
  },
  instanceId: {
    defaultValue: null,
    replace: true,
    serialize(value) {
      const int = parseInt(value);

      return !isNaN(int) ? int : this.defaultValue;
    },
    deserialize(value) {
      const int = parseInt(value);

      return !isNaN(int) ? int : this.defaultValue;
    },
  },
  ebau: {
    defaultValue: "",
    replace: true,
  },
  parcel: {
    defaultValue: "",
    replace: true,
  },
  address: {
    defaultValue: "",
    replace: true,
  },
  submitFrom: {
    defaultValue: null,
    replace: true,
    ...dateQueryParam,
  },
  submitTo: {
    defaultValue: null,
    replace: true,
    ...dateQueryParam,
  },
  order: {
    defaultValue: "camac-instance-id:desc",
    replace: true,
  },
  category: {
    defaultValue: config.APPLICATION.defaultInstanceStateCategory,
    replace: true,
  },
});

export const Mixin = queryParams.Mixin;

export default {
  queryParams,
  Mixin,
};
