import { faker } from "@faker-js/faker";

export default function graphqlId(type) {
  return btoa(`${type}:${faker.datatype.uuid()}`);
}
