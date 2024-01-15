// listening to selected text event in browser

import { ErrorMessageEvent, ExtensionEvent, SelectedTextEvent } from "../types/events";

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

  const selectedText = selection.toString().trim();
  const boundingRect = selection.getRangeAt(0).getBoundingClientRect();

  if (selectedText.length < 10) {
    chrome.runtime.sendMessage({
      type: "ERROR_MESSAGE",
      message: "Please select at least 10 characters.",
    } as ErrorMessageEvent);

    return;
  }

  chrome.runtime.sendMessage({
    type: "SELECTED_TEXT",
    selectedText,
    boundingRect,
  } as SelectedTextEvent);

  // get all selected node parents in the selection

  // get all text nodes in the selection
  // const nodes = getTextNodesForSelection(selection);
  // const selectedTexts = [];

  // add class to selected text
  // for (const node of nodes) {
  //   const container = getTextNodeContainer(node);

  //   console.log(node, node.);
  //   const textContent = node.textContent?.trim() || "";

  //   if (!container || textContent.length === 0 || !isAlphanumeric(textContent)) {
  //     // eslint-disable-next-line no-continue
  //     continue;
  //   }

  //   selectedTexts.push(textContent);

  //   // (container as HTMLElement).classList.add("hk9-highlighted");
  // }

  //   chrome.runtime.sendMessage({
  //     type: "SELECTED_TEXT",
  //     selectedTexts,
  //   } as SelectedTextEvent);
  // }
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
