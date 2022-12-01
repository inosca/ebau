import { JSONAPISerializer } from "miragejs";

export default class extends JSONAPISerializer {
  alwaysIncludeLinkageData = true;

  serialize(...args) {
    const json = super.serialize(...args);

    const {
      queryParams: { "page[number]": page, "page[size]": limit } = {},
      method,
    } = args?.[1];

    json.meta = {
      pagination: {
        page: 1,
        pages: limit ? Math.ceil(json.data.length / limit) : 1,
      },
    };

    if (method === "GET" && Array.isArray(json.data)) {
      if (page && limit) {
        const intPage = parseInt(page);
        const intLimit = parseInt(limit);

        json.meta = {
          pagination: {
            page: intPage,
            pages: Math.ceil(json.data.length / intLimit),
          },
        };

        json.data = json.data.slice(
          (intPage - 1) * intLimit,
          intPage * intLimit
        );
      }
    }
    return json;
  }
}
