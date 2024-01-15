// import { createRoot } from "react-dom/client";

// import { DOMMessage } from "../../types";
// import { Button } from "../button";

// // import "../../index.css";

// const mountButtons = (textNodes: HTMLElement[]) => {
//   for (const node of textNodes) {
//     const rootElement = document.createElement("div");
//     const uid = Math.random().toString(36).slice(2, 9);
//     const rootElementId = `hk9-extension-${uid}`;

//     rootElement.id = rootElementId;
//     rootElement.classList.add("hk9-extension");

//     if (!node.parentElement) {
//       // eslint-disable-next-line no-continue
//       continue;
//     }

//     node.parentElement.append(rootElement);

//     createRoot(rootElement).render(<Button targetElement={node} />);
//   }
// };

// const unmountButtons = () => {
//   document.querySelector("#hk9-extension-css")?.remove(); // remove css
//   document.querySelector(".hk9-extension")?.remove(); // remove root element
// };

// const getTextNodes = () => {
//   const nodeSelectors = ["h1", "h2", "h3", "h4", "h5", "h6", "p"];

//   const nodes = [...document.querySelectorAll(nodeSelectors.join(","))].filter(
//     node => node.textContent && node.textContent.length > 3
//   );

//   return [...nodes] as HTMLElement[];
// };

// const highlightTextElement: EventListener = (event: Event) => {
//   const element = event.currentTarget as HTMLElement;

//   // remove all highlighted nodes
//   const highlightedNodes = document.querySelectorAll(".hk9-highlighted");

//   for (const highlightedNode of highlightedNodes) {
//     highlightedNode.classList.remove("hk9-highlighted");
//   }

//   element.classList.add("hk9-highlighted");
// };

// const unHighlightTextElement: EventListener = (event: Event) => {
//   const element = event.currentTarget as HTMLElement;

//   element.classList.remove("hk9-highlighted");
// };

// const registerTextNodeHoverEvent = (textNodes: Element[]) => {
//   for (const node of textNodes) {
//     node.addEventListener("mouseover", highlightTextElement);

//     node.addEventListener("mouseout", unHighlightTextElement);
//   }
// };

// const unregisterTextNodeHoverEvent = (textNodes: Element[]) => {
//   for (const node of textNodes) {
//     node.removeEventListener("mouseover", highlightTextElement);

//     node.removeEventListener("mouseout", unHighlightTextElement);
//   }
// };

// const messagesFromReactAppListener = (
//   message: DOMMessage
//   // _sender: chrome.runtime.MessageSender,
//   // _sendResponse: (response: DOMMessageResponse | null) => void
// ) => {
//   const textNodes = getTextNodes();

//   // eslint-disable-next-line no-console
//   console.log("[content.js]. Message received", message);

//   switch (message.type) {
//     case "TOGGLE_EXTENSION": {
//       // eslint-disable-next-line no-console
//       console.log("[content.js]. Message response", "toggle extension");

//       if (document.querySelector("#hk9-container")) {
//         unregisterTextNodeHoverEvent(textNodes);
//         unmountButtons();
//       } else {
//         registerTextNodeHoverEvent(textNodes);
//         mountButtons(textNodes);
//       }

//       break;
//     }

//     default:
//   }
// };

// console.log(chrome.runtime);
// /**
//  * Fired when a message is sent from either an extension process or a content script.
//  */
// chrome.runtime.onMessage.addListener(messagesFromReactAppListener);

export {};
