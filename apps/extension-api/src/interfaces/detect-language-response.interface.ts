export interface DetectedLanguage {
  languageCode: string;
  confidence: number;
}

export interface DetectLanguageResponse {
  detectedLanguages: DetectedLanguage[];
}
