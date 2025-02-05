import { NextIntlClientProvider } from "next-intl";
import { PropsWithChildren } from "react";
import {
  getMessages,
  getTranslations,
  setRequestLocale,
} from "next-intl/server";
import { notFound } from "next/navigation";
import { routing } from "@/i18n/routing";
import { Titillium_Web } from "next/font/google";
import type { Metadata } from "next";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

interface Properties {
  params: {
    locale: string;
  };
}

const titilliumWeb = Titillium_Web({
  weight: ["400", "600"],
  variable: "--font-titillium-web",
  subsets: ["latin"],
});

export function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

export async function generateMetadata({
  params: { locale },
}: Properties): Promise<Metadata> {
  const t = await getTranslations({ locale, namespace: "LocaleLayout" });

  return {
    title: t("title"),
    description: t("description"),
  };
}

async function LocaleLayout({
  children,
  params: { locale },
}: Readonly<PropsWithChildren<Properties>>) {
  // Ensure that the incoming `locale` is valid
  if (!routing.locales.includes(locale as any)) {
    notFound();
  }

  // Enable static rendering
  setRequestLocale(locale);

  // Providing all messages to the client side
  const messages = await getMessages();

  return (
    <html lang={locale}>
      <body className={`${titilliumWeb.variable} antialiased`}>
        <NextIntlClientProvider messages={messages}>
          <Header />
          <main className="flex flex-col justify-center items-center w-full h-min-h py-2">
            {children}
          </main>
          <Footer />
        </NextIntlClientProvider>
      </body>
    </html>
  );
}

export default LocaleLayout;
