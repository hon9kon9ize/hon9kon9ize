import axios from "axios";

const HUGGINGFACE_INFERENCE_API = process.env.HUGGINGFACE_INFERENCE_API as string;

export const translateYue = async (text: string) => {
  try {
    const apiUrl = `${HUGGINGFACE_INFERENCE_API}/invocations`;
    const res = await axios.post<{ output: string }>(apiUrl, {
      input: text,
    });

    return res.data.output;
  } catch (error) {
    console.error(error);

    throw new Error("Failed to translate text");
  }
};
