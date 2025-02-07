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

function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

async function generateMetadata(props: Properties): Promise<Metadata> {
  const { locale } = await props.params;
  const t = await getTranslations({ locale, namespace: "LocaleLayout" });

  return {
    title: t("title"),
    description: t("description"),
  };
}

async function LocaleLayout({
  params,
  children,
}: Readonly<PropsWithChildren<Properties>>) {
  const { locale } = await params;

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
      <body className={`${titilliumWeb.variable} antialiased h-screen`}>
        <NextIntlClientProvider messages={messages}>
          <Header />
          <main className="flex flex-col items-center pt-4 pb-5 w-[75%] mx-auto h-auto">
            {children}
            <Footer />
          </main>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}

export default LocaleLayout;
export { generateStaticParams, generateMetadata };
