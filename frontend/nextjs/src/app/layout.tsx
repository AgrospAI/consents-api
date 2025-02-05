import Footer from "@/components/Footer";
import Header from "@/components/Header";
import { Geist, Geist_Mono, Titillium_Web } from "next/font/google";
import "./globals.css";
import type { Metadata } from "next";
import { PropsWithChildren } from "react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const titilliumWeb = Titillium_Web({
  weight: ["400", "600"],
  variable: "--font-titillium-web",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Consent app",
  description: "Manual consent app",
};

export default function RootLayout({ children }: Readonly<PropsWithChildren>) {
  return (
    <html lang="en">
      <body
        className={`${titilliumWeb.variable} ${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <main className="flex flex-col gap-y-4 min-h-screen w-full">
          <Header />

          <section className="flex flex-column justify-center items-center w-[75%] mx-auto">
            {children}
          </section>

          <Footer />
        </main>
      </body>
    </html>
  );
}
