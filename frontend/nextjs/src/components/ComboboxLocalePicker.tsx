import { Locale, routing } from "@/i18n/routing";
import React from "react";
import { Popover, PopoverTrigger } from "@/components/ui/popover";
import Flag from "@/components/Flag";
import { ChevronUp, ChevronDown } from "lucide-react";
import { PopoverContent } from "@radix-ui/react-popover";
import { Command, CommandGroup, CommandList } from "@/components/ui/command";
import { CommandItem } from "cmdk";
import { useTranslations } from "use-intl";

interface Properties {
  locale: Locale;
  updateLocale: (locale: Locale) => void;
  isOpen: boolean;
  isPending: boolean;
  setIsOpen: (isOpen: boolean) => void;
}

function ComboboxLocalePicker({
  isPending,
  locale,
  updateLocale,
  isOpen,
  setIsOpen,
}: Properties) {
  const t = useTranslations("LocalePicker");

  return (
    <Popover onOpenChange={() => setIsOpen(!isOpen)}>
      <PopoverTrigger asChild disabled={isPending}>
        <div className="flex flex-row gap-x-1 items-center justify-center cursor-pointer hover:scale-105">
          <Flag locale={locale} className="size-8" />
          {isOpen ? <ChevronUp /> : <ChevronDown />}
        </div>
      </PopoverTrigger>
      <PopoverContent>
        <Command>
          <CommandList>
            <CommandGroup className="w-32 shadow-md p-2">
              {routing.locales.map((curr, idx) => (
                <CommandItem
                  key={idx}
                  value={curr}
                  onSelect={(curr) => {
                    updateLocale(curr as Locale);
                    setIsOpen(false);
                  }}
                  className={`flex flex-col gap-4 cursor-pointer transition duration-100 hover:scale-105 ${
                    curr == locale
                      ? "bg-primary text-white"
                      : "bg-white text-black"
                  }`}
                >
                  <div
                    className={`flex flex-row gap-x-4 items-center justify-start bold w-auto text-md hover:underline underline-offset-2 ${
                      curr == locale
                        ? "text-white hover:text-secondary"
                        : "text-black hover:text-primary"
                    }`}
                  >
                    <Flag locale={curr} className="size-8" />
                    <p className="uppercase">{t(curr)}</p>
                  </div>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}

export default ComboboxLocalePicker;
