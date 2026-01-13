import Transform from "@ember-data/serializer/transform";

export default class JournalVisibilityTransform extends Transform {
  deserialize(serialized) {
    switch (serialized) {
      case "authorities":
        return true;
      case "own_organization":
        return false;
      default:
        return false;
    }
  }

  serialize(deserialized) {
    if (deserialized) {
      return "authorities";
    }

    return "own_organization";
  }
}
