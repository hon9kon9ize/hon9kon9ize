export interface TTSResponse {
  mp3Buffer: Buffer;
  speechMarks: SpeechMark[];
}

export interface SpeechMark {
  time: number;
  type: string;
  start: number;
  end: number;
  value: string;
}
