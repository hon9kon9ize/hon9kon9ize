import clsx from "clsx";
import { FC } from "react";

interface ButtonContentProps {
  top: number;
  left: number;
  active?: boolean;
}

export const ButtonContent: FC<ButtonContentProps> = ({ top, left, active }) => {
  return (
    <div
      className={clsx([
        "-translate-x-full",
        "-translate-y-full",
        "absolute",
        "w-auto",
        "h-auto",
        "duration-300",
        ...(active ? ["animate-in", "fade-in"] : ["hidden"]),
      ])}
      style={{
        pointerEvents: "all",
        top: `${top}px`,
        left: `${left}px`,
      }}
    >
      Test3
    </div>
  );
};
