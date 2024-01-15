import { Datastore } from "@google-cloud/datastore";
import { Storage } from "@google-cloud/storage";

const datastore = new Datastore();
const storage = new Storage();
const GCP_BUCKET_NAME = process.env.GCP_BUCKET_NAME as string;

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
    const cacheItem = {
      value: JSON.stringify(value),
      ...(ttl && { ttl: new Date(Date.now() + ttl) }),
    };

    await datastore.save({
      key: datastore.key(["Cache", key]),
      data: cacheItem,
    });
  },
};

export const FileCache = {
  async get(key: string): Promise<Buffer | null> {
    const [doesFileExist] = await storage.bucket(GCP_BUCKET_NAME).file(key).exists();

    if (!doesFileExist) {
      return null;
    }

    const [cacheItem] = await storage.bucket(GCP_BUCKET_NAME).file(key).download();

    if (!cacheItem) {
      return null;
    }

    return Buffer.from(cacheItem.buffer);
  },

  async set(key: string, value: Buffer) {
    await storage.bucket(GCP_BUCKET_NAME).file(key).save(value);

    return value;
  },
};
