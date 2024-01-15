import { FC, useEffect, useMemo, useState } from "react";
import { clsx } from "clsx";
import { ButtonContent } from "./button-content";

const PADDING = 5;

export const Button: FC<{ targetElement?: HTMLElement; className?: string }> = ({
  targetElement,
  className,
}) => {
  const [browserSize, setBrowserSize] = useState([window.innerWidth, window.innerHeight]);
  const [isButtonActive, setIsButtonActive] = useState(false);
  const targetElementBox = useMemo(() => {
    if (!targetElement || !targetElement.parentElement) {
      return {
        top: 0,
        left: 0,
        parentTop: 0,
        parentLeft: 0,
        width: 0,
        height: 0,
        parentWidth: 0,
        parentHeight: 0,
      };
    }

    const { width, height } = targetElement.getBoundingClientRect();
    const { width: parentWidth, height: parentHeight } =
      targetElement.parentElement.getBoundingClientRect();
    const left = Math.round(targetElement.offsetLeft);
    const top = Math.round(targetElement.offsetTop);
    const parentLeft = Math.round(targetElement.parentElement.offsetLeft);
    const parentTop = Math.round(targetElement.parentElement.offsetTop);

    return {
      top: top - parentTop,
      left: left - parentLeft,
      parentTop,
      parentLeft,
      width,
      height,
      parentWidth,
      parentHeight,
    };
  }, [targetElement, browserSize]); // re-calculate when targetElement or browserSize changes

  useEffect(() => {
    // add event listener to browser resize
    const resizeHandler = () => {
      setBrowserSize([window.innerWidth, window.innerHeight]);
    };

    const onTargetElementMouseOver = () => {
      setIsButtonActive(true);
    };

    const onTargetElementMouseOut = () => {
      setIsButtonActive(false);
    };

    window.addEventListener("resize", resizeHandler);

    if (targetElement) {
      targetElement.addEventListener("mouseover", onTargetElementMouseOver);

      targetElement.addEventListener("mouseout", onTargetElementMouseOut);
    }

    return () => {
      window.removeEventListener("resize", resizeHandler);

      if (targetElement) {
        targetElement.removeEventListener("mouseover", onTargetElementMouseOver);

        targetElement.removeEventListener("mouseout", onTargetElementMouseOut);
      }
    };
  }, [targetElement]);

  return (
    <div
      className={clsx(["hk9-extension-button", "absolute", "top-0", "left-0", "z-[1]", className])}
    >
      <div
        className={clsx([
          "absolute",
          "box-content",
          "overflow-hidden",
          "pointer-events-none",
          "border-0",
          "rounded-none",
          "p-0",
          "m-0",
          className,
        ])}
        style={{
          top: `${targetElementBox.parentTop}px`,
          left: `${targetElementBox.parentLeft}px`,
          width: `${targetElementBox.parentWidth}px`,
          height: `${targetElementBox.parentHeight}px`,
        }}
      >
        <div
          className={clsx([
            "absolute",
            "box-content",
            "overflow-hidden",
            "pointer-events-none",
            "border-0",
            "rounded-none",
            "p-0",
            "m-0",
          ])}
          style={{
            top: `${targetElementBox.top}px`,
            left: `${targetElementBox.left}px`,
            width: `${targetElementBox.width}px`,
            height: `${targetElementBox.height}px`,
          }}
        >
          <ButtonContent
            active={isButtonActive}
            left={targetElementBox.width - PADDING}
            top={targetElementBox.height - PADDING}
          />
        </div>
      </div>
    </div>
  );
};
