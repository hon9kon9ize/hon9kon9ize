import { PollyClient, SynthesizeSpeechCommand } from "@aws-sdk/client-polly";
import { SpeechMark } from "../interfaces";

const AWS_DEFAULT_REGION = process.env.AWS_DEFAULT_REGION as string;

const client = new PollyClient({
  region: AWS_DEFAULT_REGION,
});

export interface TTSItem {
  mp3Buffer: Buffer;
  speechMarks: SpeechMark[];
}

export const tts = async (text: string): Promise<TTSItem> => {
  const voiceId = "Hiujin";
  const engine = "neural";

  const mp3Data = await client.send(
    new SynthesizeSpeechCommand({
      Engine: engine,
      OutputFormat: "mp3",
      Text: text,
      VoiceId: voiceId,
    })
  );

  if (!mp3Data.AudioStream) {
    throw new Error("Failed to get mp3 data");
  }

  const jsonData = await client.send(
    new SynthesizeSpeechCommand({
      Engine: engine,
      OutputFormat: "json",
      Text: text,
      VoiceId: voiceId,
      SpeechMarkTypes: ["word"],
    })
  );

  if (!jsonData.AudioStream) {
    throw new Error("Failed to get speech mark data");
  }

  const mp3Buffer = Buffer.from(await mp3Data.AudioStream.transformToByteArray());
  const speechMarksBuffer = Buffer.from(await jsonData.AudioStream.transformToByteArray()).toString(
    "utf8"
  );
  const speechMarks = JSON.parse(
    `[${speechMarksBuffer.trim().replaceAll("\n", ",")}]`
  ) as SpeechMark[];

  return {
    mp3Buffer,
    speechMarks,
  };
};
