import Frame from "react-frame-component";
import { createRoot } from "react-dom/client";
// listening to selected text event in browser

import { ErrorMessageEvent, ExtensionEvent, SelectedTextEvent } from "../types/events";

const createConfirmButtons = (selection: Selection) => {
  // remove all previous buttons
  const buttonsContainers = document.querySelectorAll(".hk9-buttons-container");

  for (const container of buttonsContainers) {
    container.remove();
  }

  // calculate the global position of the selected text
  const range = selection.getRangeAt(0);
  const rect = range.getBoundingClientRect();

  console.log("selectedText =", selectedText);

  buttonsContainer.classList.add("hk9-buttons-container");
  buttonsContainer.style.top = `${rect.top}px`;
  buttonsContainer.style.left = `${rect.left}px`;
  buttonsContainer.style.width = `100px`;
  buttonsContainer.style.height = `100px`;
  buttonsContainer.style.position = "absolute";
  buttonsContainer.style.zIndex = "9999";

  document.body.append(buttonsContainer);

  createRoot(buttonsContainer).render(
    <Frame>
      <div>hello</div>
    </Frame>
  );
};

const handleSelectedText = () => {
  const selection = window.getSelection();

  // clear all highlighted text
  const highlightedNodes = document.querySelectorAll(".hk9-highlighted");

  for (const highlightedNode of highlightedNodes) {
    highlightedNode.classList.remove("hk9-highlighted");
  }

  if (!selection || selection.isCollapsed) {
    return;
  }

  createConfirmButtons(selection);
};

const registerListeners = () => {
  document.addEventListener("mouseup", handleSelectedText);
  document.addEventListener("keyup", handleSelectedText);
  document.addEventListener("touchend", handleSelectedText);
};

const unregisterListeners = () => {
  document.removeEventListener("mouseup", handleSelectedText);
  document.removeEventListener("keyup", handleSelectedText);
  document.removeEventListener("touchend", handleSelectedText);
};

chrome.runtime.sendMessage(
  {
    type: "INIT_EXTENSION",
  } as ExtensionEvent,
  response => {
    if (response.enabled) {
      registerListeners();
    }
  }
);

chrome.runtime.onMessage.addListener((message: ExtensionEvent) => {
  switch (message.type) {
    case "TOGGLE_EXTENSION": {
      if (message.enabled) {
        registerListeners();
        handleSelectedText();
      } else {
        unregisterListeners();
      }

      break;
    }

    default:
  }
});

export {};
