import React, { useState, useTransition } from "react";
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer";
import Flag from "@/components/Flag";
import { Button } from "@/components/ui/button";
import { useLocale, useTranslations } from "next-intl";
import { Locale, routing, useRouter, usePathname } from "@/i18n/routing";
import { ChevronDown, ChevronUp } from "lucide-react";
import { useParams } from "next/navigation";

function LocalePicker() {
  const t = useTranslations("LocalePicker");
  const router = useRouter();
  const locale = useLocale();

  const pathname = usePathname();
  const params = useParams();

  const locales = routing.locales;
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
    <Drawer onOpenChange={() => setIsOpen(!isOpen)}>
      <DrawerTrigger>
        <div className="flex flex-row gap-x-1 items-center justify-center">
          <Flag locale={locale} className="size-8" />
          {isOpen ? <ChevronUp /> : <ChevronDown />}
        </div>
      </DrawerTrigger>
      <DrawerContent className="flex flex-col items-center ">
        <DrawerHeader>
          <DrawerTitle>{t("title")}</DrawerTitle>
          <DrawerDescription>{t("description")}</DrawerDescription>
        </DrawerHeader>
        <div className="flex flex-col gap-y-4">
          {locales.map((locale, idx) => (
            <DrawerClose key={idx} asChild>
              <Button
                className="flex flex-row gap-x-4 items-center justify-start bold w-32 text-md hover:underline underline-offset-2"
                onClick={() => onLocaleChange(locale)}
              >
                <Flag locale={locale} />
                <p className="uppercase ">{t(locale)}</p>
              </Button>
            </DrawerClose>
          ))}
        </div>
        <DrawerFooter>
          <DrawerClose asChild>
            <Button variant="destructive">{t("cancel")}</Button>
          </DrawerClose>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  );
}

export default LocalePicker;
