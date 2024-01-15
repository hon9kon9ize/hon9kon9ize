export type ToggleExtensionEvent = {
  type: "TOGGLE_EXTENSION";
  enabled: boolean;
};

export type InitExtensionEvent = {
  type: "INIT_EXTENSION";
};

export type InitExtensionEventResponse = {
  enabled: boolean;
};

export type ErrorMessageEvent = {
  type: "ERROR_MESSAGE";
  message: string;
};

export type SelectedTextEvent = {
  type: "SELECTED_TEXT";
  selectedText: string;
  boundingRect: DOMRect;
  lang: string; // language code ISO 639-1
};

export type ExtensionEvent =
  | ToggleExtensionEvent
  | InitExtensionEvent
  | SelectedTextEvent
  | ErrorMessageEvent;
