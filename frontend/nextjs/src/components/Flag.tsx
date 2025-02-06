import * as Flags from "country-flag-icons/react/3x2";
import React from "react";

interface Properties {
  locale: string;
  className?: string;
  name?: string;
}

const countryCodes = {
  en: "gb",
  es: "es",
};

function Flag({ locale, className, name }: Properties) {
  console.log(locale, name);
  const FlagComponent =
    Flags[
      countryCodes[
        locale as keyof typeof countryCodes
      ].toUpperCase() as keyof typeof Flags
    ];
  return <FlagComponent className={className} />;
}

export default Flag;
