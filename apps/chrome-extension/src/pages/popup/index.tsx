import { createRoot } from "react-dom/client";
import Popup from "./popup";
import "./index.css";

const root = document.createElement("div");

root.id = "popup-root";
document.querySelector("#hk9-popup-container")?.append(root);

createRoot(root).render(<Popup />);
