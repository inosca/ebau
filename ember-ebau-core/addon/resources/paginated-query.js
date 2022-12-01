import { registerDestructor } from "@ember/destroyable";
import { inject as service } from "@ember/service";
import { task, lastValue } from "ember-concurrency";
import { Resource } from "ember-resources";

const getQueryDiff = (oldQuery, newQuery) =>
  [...Object.keys(oldQuery), ...Object.keys(newQuery)].reduce(
    (diff, currentKey) => ({
      ...diff,
      ...(oldQuery[currentKey] !== newQuery[currentKey]
        ? { [currentKey]: oldQuery[currentKey] }
        : {}),
    }),
    {}
  );

const shouldResetPage = ([oldModel, oldQuery] = [], [newModel, newQuery]) =>
  parseInt(newQuery.page.number) === 1 ||
  oldModel !== newModel ||
  Object.keys(getQueryDiff(oldQuery, newQuery)).filter((key) => key !== "page")
    .length;

export default (context, modelName, query) =>
  PaginatedQuery.from(context, () => [modelName, query()]);

export class PaginatedQuery extends Resource {
  @service store;

  get records() {
    return this.data?.records ?? [];
  }

  get isLoading() {
    return this.fetchData.isRunning;
  }

  get hasMore() {
    return this.data?.hasMore;
  }

  get error() {
    return this.data.error;
  }

  get isError() {
    return Boolean(this.error);
  }

  constructor(owner) {
    super(owner);

    registerDestructor(this, () => {
      this.fetchData.cancelAll({ resetState: true });
    });
  }

  modify(positional) {
    this.fetchData.perform(...positional);
  }

  @lastValue("fetchData") data;
  fetchData = task({ restartable: true }, async (model, query) => {
    await Promise.resolve();
    try {
      const data = await this.store.query(model, query);

      return {
        records: shouldResetPage(this.fetchData.lastSuccessful?.args, [
          model,
          query,
        ])
          ? data.toArray()
          : [...this.data.records.toArray(), ...data.toArray()],
        hasMore: query.page.number < data.meta?.pagination?.pages ?? false,
      };
    } catch (error) {
      console.error(error);
      return { isError: true, error };
    }
  });
}
