import * as crypto from "crypto";

export const md5hash = (data: string) => {
  return crypto.createHash("md5").update(data).digest("hex");
};
