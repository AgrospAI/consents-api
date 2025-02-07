"use client";
import { Link, usePathname } from "@/i18n/routing";
import { TableOfContents, User } from "lucide-react";
import { useTranslations } from "next-intl";
import React, { PropsWithChildren, ReactElement } from "react";

interface PageLink {
  href: string;
  label: string;
  icon: ReactElement;
}

const links: PageLink[] = [
  { href: "/consents", label: "consents", icon: <TableOfContents /> },
  { href: "/profile", label: "profile", icon: <User /> },
];

function Navigation({ children }: Readonly<PropsWithChildren>) {
  const t = useTranslations("Header");
  const pathname = usePathname();

  return (
    <nav className="flex px-3 text-sm justify-center items-center gap-x-8 font-bold text-secondary">
      {links.map(({ href, label, icon }, index) => (
        <Link
          key={index}
          aria-label={label}
          className="uppercase transform transition hover:underline underline-offset-4 flex items-center gap-x-2  hover:scale-105"
          href={href}
        >
          {icon} {t(label)}
        </Link>
      ))}
      {children}
    </nav>
  );
}

export default Navigation;
