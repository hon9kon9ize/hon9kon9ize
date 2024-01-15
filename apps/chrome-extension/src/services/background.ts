import { ExtensionEvent, InitExtensionEventResponse } from "../types/events";

const STORAGE_TOGGLE_CHECKED_KEY = "STORAGE_TOGGLE_CHECKED_KEY";

chrome.runtime.onMessage.addListener((message: ExtensionEvent, _sender, sendResponse) => {
  console.log("[background.ts]. Message received", message);

  switch (message.type) {
    case "INIT_EXTENSION": {
      chrome.storage.sync.get(
        [STORAGE_TOGGLE_CHECKED_KEY],
        ({ [STORAGE_TOGGLE_CHECKED_KEY]: enabled }) => {
          const response: InitExtensionEventResponse = {
            enabled: !!enabled,
          };

          sendResponse(response);
        }
      );
      break;
    }

    case "SELECTED_TEXT": {
      // eslint-disable-next-line no-console
      console.log("[background.js]. Selected text", message.selectedText);
      break;
    }

    case "TOGGLE_EXTENSION": {
      chrome.storage.sync.set({ [STORAGE_TOGGLE_CHECKED_KEY]: message.enabled });
      break;
    }

    default: {
      break;
    }
  }

  return true;
});

console.log("[background.ts]. This is the background page.");

export {};
