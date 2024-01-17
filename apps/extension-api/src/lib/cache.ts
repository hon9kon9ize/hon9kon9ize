import { Datastore } from "@google-cloud/datastore";

const datastore = new Datastore();

export const KeyValueCache = {
  async get<V = any>(key: string): Promise<V | null> {
    const [cacheValue] = await datastore.get(datastore.key(["Cache", key]));

    if (!cacheValue) {
      return null;
    }

    try {
      const value = JSON.parse(cacheValue.value);

      return value;
    } catch {
      return null;
    }
  },

  async set<V = any>(key: string, value: V, ttl?: number): Promise<void> {
    const data = {
      value: JSON.stringify(value),
      ...(ttl && { ttl: new Date(Date.now() + ttl) }),
    };

    await datastore.save({
      key: datastore.key(["Cache", key]),
      data,
    });
  },
};
