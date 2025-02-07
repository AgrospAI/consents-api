"use client";

import { PropsWithChildren, useState } from "react";
import "./globals.css";
import AuthContext from "@/context";
import User from "@/lib/entities/User";

function RootLayout({ children }: Readonly<PropsWithChildren>) {
  const [user, setUser] = useState<User>();

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export default RootLayout;
