"use client";

import React, { useState, useTransition } from "react";
import { useLocale } from "next-intl";
import { Locale, useRouter, usePathname } from "@/i18n/routing";
import { useParams } from "next/navigation";
import DrawerLocalePicker from "./DrawerLocalePicker";
import ComboboxLocalePicker from "./ComboboxLocalePicker";

function LocalePicker() {
  const router = useRouter();
  const locale = useLocale() as Locale;

  const pathname = usePathname();
  const params = useParams();

  const [isOpen, setIsOpen] = useState(false);
  const [isPending, startTransition] = useTransition();

  function onLocaleChange(nextLocale: Locale) {
    startTransition(() => {
      router.replace(
        // @ts-expect-error -- TypeScript will validate that only known `params`
        // are used in combination with a given `pathname`. Since the two will
        // always match for the current route, we can skip runtime checks.
        { pathname, params },
        { locale: nextLocale }
      );
    });
  }

  return (
    <>
      <div className="lg:hidden">
        <DrawerLocalePicker
          locale={locale}
          updateLocale={onLocaleChange}
          isOpen={isOpen}
          setIsOpen={setIsOpen}
          isPending={isPending}
        />
      </div>
      <div className="hidden lg:block z-1000">
        <ComboboxLocalePicker
          locale={locale}
          updateLocale={onLocaleChange}
          isOpen={isOpen}
          setIsOpen={setIsOpen}
          isPending={isPending}
        />
      </div>
    </>
  );
}

export default LocalePicker;
