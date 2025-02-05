import { PropsWithChildren } from "react";
import "./globals.css";

function RootLayout({ children }: Readonly<PropsWithChildren>) {
  return children;
}

export default RootLayout;
