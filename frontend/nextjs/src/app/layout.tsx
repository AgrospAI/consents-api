"use client";

import { PropsWithChildren, useState } from "react";
import "./globals.css";
import AuthProvider from "@/context/AuthProvider";
import User from "@/utils/entities/User";
import Web3Provider from "@/context/Web3Provider";

function RootLayout({ children }: Readonly<PropsWithChildren>) {
  const [user, setUser] = useState<User>();

  return (
    <Web3Provider>
      <AuthProvider.Provider value={{ user, setUser }}>
        {children}
      </AuthProvider.Provider>
    </Web3Provider>
  );
}

export default RootLayout;
