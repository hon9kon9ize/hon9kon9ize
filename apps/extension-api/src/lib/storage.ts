import { Storage as GoogleCloudStorage } from "@google-cloud/storage";

export const storage = new GoogleCloudStorage();
export const GCP_BUCKET_NAME = process.env.GCP_BUCKET_NAME as string;
export const CDN_URL = process.env.CDN_URL as string;

export const Storage = {
  async getUrl(key: string): Promise<string | null> {
    const [doesFileExist] = await storage.bucket(GCP_BUCKET_NAME).file(key).exists();

    if (!doesFileExist) {
      return null;
    }

    const [signedUrl] = await storage
      .bucket(GCP_BUCKET_NAME)
      .file(key)
      .getSignedUrl({
        action: "read",
        cname: CDN_URL,
        expires: Date.now() + 1000 * 60 * 60, // 1 hour
      });

    if (!signedUrl) {
      return null;
    }

    return signedUrl;
  },

  async get(key: string): Promise<Buffer | null> {
    const [doesFileExist] = await storage.bucket(GCP_BUCKET_NAME).file(key).exists();

    if (!doesFileExist) {
      return null;
    }

    const [file] = await storage.bucket(GCP_BUCKET_NAME).file(key).download();

    if (!file) {
      return null;
    }

    return file;
  },

  async set(key: string, value: Buffer): Promise<void> {
    await storage.bucket(GCP_BUCKET_NAME).file(key).save(value);
  },
};
