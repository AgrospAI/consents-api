import React, { PropsWithChildren } from "react";
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
import { ChevronUp, ChevronDown } from "lucide-react";
import Flag from "@/components/Flag";
import { Button } from "./ui/button";
import { Locale, routing } from "@/i18n/routing";
import { useTranslations } from "next-intl";

interface Properties {
  isPending: boolean;
  locale: Locale;
  updateLocale: (locale: Locale) => void;
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
}

function DrawerLocalePicker({
  isPending,
  locale,
  updateLocale,
  isOpen,
  setIsOpen,
}: Properties) {
  const t = useTranslations("LocalePicker");

  return (
    <Drawer onOpenChange={() => setIsOpen(!isOpen)}>
      <DrawerTrigger disabled={isPending}>
        <div className="flex flex-row gap-x-1 items-center justify-center">
          <Flag locale={locale} className="size-8" />
          {isOpen ? <ChevronUp /> : <ChevronDown />}
        </div>
      </DrawerTrigger>
      <DrawerContent className="flex flex-col items-center">
        <DrawerHeader>
          <DrawerTitle>{t("title")}</DrawerTitle>
          <DrawerDescription>{t("description")}</DrawerDescription>
        </DrawerHeader>
        <div className="flex flex-col gap-y-4">
          {routing.locales.map((curr, idx) => (
            <DrawerClose key={idx} asChild>
              <Button
                className="flex flex-row gap-x-4 items-center justify-start bold w-32 text-md hover:underline hover:scale-105 underline-offset-2"
                onClick={() => updateLocale(curr)}
              >
                <Flag locale={curr} className="size-8" />
                {t(curr)}
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

export default DrawerLocalePicker;
