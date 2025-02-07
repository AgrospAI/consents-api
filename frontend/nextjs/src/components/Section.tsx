import React, { PropsWithChildren } from "react";

function Section({
  children,
  ...props
}: Readonly<PropsWithChildren & React.HTMLAttributes<HTMLElement>>) {
  return <section {...props}>{children}</section>;
}

export default Section;
