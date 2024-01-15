import { useEffect, useState } from "react";
import type { InitExtensionEventResponse, ToggleExtensionEvent } from "../../types/events";
import Logo from "./logo.svg";

const TOGGLE_ID = "hk9-popup-toggle";

export default function Popup() {
  const [toggleChecked, setToggleChecked] = useState(false);

  const handleToggleOnChange: React.ChangeEventHandler<HTMLInputElement> = event => {
    const { checked } = event.currentTarget;

    setToggleChecked(checked);

    chrome.runtime.sendMessage({
      type: "TOGGLE_EXTENSION",
      enabled: checked,
    } as ToggleExtensionEvent);
  };

  useEffect(() => {
    // eslint-disable-next-line promise/catch-or-return
    chrome.runtime
      .sendMessage({
        type: "INIT_EXTENSION",
      })
      // eslint-disable-next-line promise/always-return
      .then((response: InitExtensionEventResponse) => {
        setToggleChecked(response.enabled);
      });
  }, []);

  return (
    <div className="font-space-mono min-h-[200px] flex flex-col gap-2">
      <nav className="border-b border-slate-300 p-4">
        <div id="hk9-logo">
          <img alt="Logo" className="fill-current" src={Logo} width="220" />
        </div>
      </nav>
      <div className="flex flex1 flex-col gap-2 p-4">
        <h2 className="text-black uppercase text-lg">Settings</h2>
        <div className="flex flex-row gap-2 items-center">
          {/* eslint-disable-next-line jsx-a11y/label-has-associated-control */}
          <label className="text-black flex-1 text-sm" htmlFor={TOGGLE_ID}>
            Translate highlighted text to Cantonese
          </label>
          <input
            checked={toggleChecked}
            className="peer relative shrink-0 w-11 h-6 p-px bg-gray-200 border-transparent text-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:ring-black disabled:opacity-50 disabled:pointer-events-none checked:bg-none checked:text-black checked:border-black focus:checked:border-black dark:bg-gray-800 dark:border-gray-700 dark:checked:bg-primary-500 dark:checked:border-primary-500 dark:focus:ring-offset-gray-600 before:inline-block before:w-5 before:h-5 before:bg-white checked:before:bg-primary-200 before:translate-x-0 checked:before:translate-x-full before:rounded-full before:shadow before:transform before:ring-0 before:transition before:ease-in-out before:duration-200 dark:before:bg-gray-400 dark:checked:before:bg-primary-200"
            id={TOGGLE_ID}
            type="checkbox"
            onChange={handleToggleOnChange}
          />
        </div>
      </div>
    </div>
  );
}
