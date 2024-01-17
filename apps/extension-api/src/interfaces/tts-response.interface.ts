export interface TTSResponse {
  mp3Url: string;
  speechMarksUrl: string;
}

export interface SpeechMark {
  time: number;
  type: string;
  start: number;
  end: number;
  value: string;
}
