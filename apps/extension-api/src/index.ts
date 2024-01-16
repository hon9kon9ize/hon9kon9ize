import "dotenv/config";

import { v3beta1 } from "@google-cloud/translate";
import express, { Request, Response } from "express";
import tags from "language-tags";
import { slowDown } from "express-slow-down";
import { google } from "@google-cloud/translate/build/protos/protos";
import {
  DetectLanguageRequest,
  DetectLanguageResponse,
  DetectedLanguage,
  ErrorResponse,
  TTSResponse,
  TranslateItem,
  TranslateTextRequestBody,
  TranslateTextResponse,
} from "./interfaces";
import { FileCache, KeyValueCache, md5hash, tts } from "./lib";
import { translateYue } from "./lib/translate-yue";

const GCP_PROJECT_ID = process.env.GCP_PROJECT_ID as string;

const app = express();
const v1Route = express.Router();
let supportedLanguages: google.cloud.translation.v3beta1.ISupportedLanguages;

const translationClient = new v3beta1.TranslationServiceClient();

// register rate limit middleware
const rateLimitMiddleware = slowDown({
  windowMs: 60 * 1000, // 1 minute
  delayAfter: 20, // allow 20 requests per minute
  delayMs: hits => hits * 100, // add 100 ms of delay to every request after the 5th one.
});

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(rateLimitMiddleware);
app.use("/v1", v1Route);

app.get("/", (_req: Request, res: Response) => {
  res.redirect("https://www.hon9kon9ize.com");
});

v1Route.post("/tts", async (req: Request, res: Response<TTSResponse | ErrorResponse>) => {
  const { text } = req.body;

  if (!text) {
    res.status(400).send({ message: "text is required" });

    return;
  }

  try {
    // find cache from cache storage
    const cacheKey = md5hash(`${text}`);
    const cacheFileKey = `${cacheKey}.mp3`;
    const cacheSpeechMarksKey = `${cacheKey}.json`;
    const cachedMp3File = await FileCache.get(cacheFileKey);
    const cachedSpeechMarks = await FileCache.get(cacheSpeechMarksKey);

    if (cachedMp3File !== null && cachedSpeechMarks !== null) {
      console.info("cache hit");

      res.status(200).send({
        mp3Buffer: cachedMp3File,
        speechMarks: JSON.parse(cachedSpeechMarks.toString()),
      });

      return;
    }

    const { mp3Buffer, speechMarks } = await tts(text); // mp3 audio buffer

    if (!mp3Buffer) {
      res.status(500).send({ message: "tts error" });

      return;
    }

    // save cache to cache storage
    await FileCache.set(cacheFileKey, mp3Buffer);
    await FileCache.set(cacheSpeechMarksKey, Buffer.from(JSON.stringify(speechMarks)));

    res.status(200).send({
      mp3Buffer,
      speechMarks,
    });
  } catch (error) {
    console.error(error);
    res.status(500).send({ message: "tts error" });
  }
});

v1Route.post(
  "/translate-yue",
  async (req: Request, res: Response<TranslateTextResponse | ErrorResponse>) => {
    const { text } = req.body;

    if (!text) {
      res.status(400).send({ message: "text is required" });

      return;
    }

    try {
      const translatedText = await translateYue(text);

      res.status(200).send({
        translatedText,
      });
    } catch (error) {
      console.error(error);
      res.status(500).send({ message: "translation error" });
    }
  }
);

v1Route.post(
  "/detect-language",
  async (
    req: Request<any, any, DetectLanguageRequest>,
    res: Response<DetectLanguageResponse | ErrorResponse>
  ) => {
    const { text } = req.body;

    if (!text) {
      res.status(400).send({ message: "text is required" });

      return;
    }

    try {
      const [detectionResult] = await translationClient.detectLanguage({
        parent: `projects/${GCP_PROJECT_ID}/locations/global`,
        content: text,
        mimeType: "text/plain",
      });

      res.status(200).send({
        detectedLanguages: detectionResult.languages
          ?.filter(l => l.confidence && l.languageCode)
          .map(l => ({
            languageCode: l.languageCode,
            confidence: l.confidence,
          })) as DetectedLanguage[],
      });
    } catch (error) {
      console.error(error);
      res.status(500).send({ message: "translation error" });
    }
  }
);

v1Route.post(
  "/translate",
  async (
    req: Request<any, any, TranslateTextRequestBody>,
    res: Response<TranslateTextResponse | ErrorResponse>
  ) => {
    const { text, language, url, siteTitle } = req.body;

    if (!text) {
      res.status(400).send({ message: "text is required" });

      return;
    }

    if (language && !tags(language).valid()) {
      res.status(400).send({ message: "language is invalid" });

      return;
    }

    try {
      // find cache from datastore
      const cacheKey = `${md5hash(`${text}:${language}`)}`;
      const cachedItem = (await KeyValueCache.get(`${cacheKey}`)) as TranslateItem;

      if (!supportedLanguages) {
        [supportedLanguages] = await translationClient.getSupportedLanguages({
          parent: `projects/${GCP_PROJECT_ID}/locations/global`,
          displayLanguageCode: "en",
        });
      }

      if (supportedLanguages.languages?.findIndex(l => l.languageCode === language) === -1) {
        res.status(400).send({ message: "language is not supported" });

        return;
      }

      if (cachedItem) {
        console.info("cache hit");

        res.status(200).send({
          translatedText: cachedItem.translatedText,
        });

        return;
      }

      const translatedTextRequest: google.cloud.translation.v3beta1.ITranslateTextRequest = {
        parent: `projects/${GCP_PROJECT_ID}/locations/global`,
        contents: [text],
        mimeType: "text/plain",
        sourceLanguageCode: language,
        targetLanguageCode: "zh",
      };

      if (language) {
        translatedTextRequest.sourceLanguageCode = language;
      }

      const [translatedTextResponse] = await translationClient.translateText(translatedTextRequest);
      const translatedText = translatedTextResponse.translations?.[0].translatedText;

      if (!translatedText) {
        res.status(500).send({ message: "translation error" });

        return;
      }

      // save cache to datastore
      await KeyValueCache.set(cacheKey, { translatedText, language, url, siteTitle });

      res.status(200).send({
        translatedText,
      });
    } catch (error) {
      console.error(error);
      res.status(500).send({ message: "translation error" });
    }
  }
);

app.listen(8081, () => {
  console.info("server started at http://localhost:8081");
});
