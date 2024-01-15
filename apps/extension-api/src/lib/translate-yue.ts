import axios from "axios";
import { URL } from "url";
import { GoogleAuth } from "google-auth-library";

const HUGGINGFACE_INFERENCE_API_URL = process.env.HUGGINGFACE_INFERENCE_API_URL as string;

export const getGoogleCloudAccessToken = async (): Promise<string> => {
  try {
    const targetAudience = new URL(HUGGINGFACE_INFERENCE_API_URL).origin;
    const auth = new GoogleAuth();
    const client = await auth.getIdTokenClient(targetAudience);
    const idToken = await client.idTokenProvider.fetchIdToken(targetAudience);

    if (!idToken) {
      throw new Error("Failed to get Google Cloud access token");
    }

    return idToken;
  } catch (error) {
    console.error(error);

    throw new Error("Failed to get Google Cloud access token");
  }
};

export const translateYue = async (text: string) => {
  try {
    const accessToken = await getGoogleCloudAccessToken();
    const res = await axios.post<{ output: string }>(
      HUGGINGFACE_INFERENCE_API_URL,
      {
        input: text,
      },
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    return res.data.output;
  } catch (error) {
    console.error(error);

    throw new Error("Failed to translate text");
  }
};
