import { isEmpty } from "@ember/utils";

export default function cleanObject(obj) {
  return Object.entries(obj).reduce((clean, [key, value]) => {
    return {
      ...clean,
      ...(isEmpty(value) ? {} : { [key]: value }),
    };
  }, {});
}
