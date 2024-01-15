declare module "*.svg" {
  import React = require("react");

  export const ReactComponent: React.SFC<React.SVGProps<SVGSVGElement>>;
  const source: string;

  export default source;
}

declare module "*.jpg" {
  const content: string;

  export default content;
}

declare module "*.png" {
  const content: string;

  export default content;
}

declare module "*.json" {
  const content: string;

  export default content;
}
