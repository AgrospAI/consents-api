"use client";

import Image from "next/image";
import logo from "@public/logo-horizontal.svg";
import { TableOfContents, User } from "lucide-react";
import { ReactElement } from "react";
import { Link } from "@/i18n/routing";
import { useTranslations } from "next-intl";
import { useParams } from "next/navigation";
import LocalePicker from "@/components/LocalePicker";

interface PageLink {
  href: string;
  label: string;
  icon: ReactElement;
}

const links: PageLink[] = [
  { href: "/", label: "consents", icon: <TableOfContents /> },
  { href: "/profile", label: "profile", icon: <User /> },
];

function Header() {
  const t = useTranslations("Header");
  const { locale } = useParams<{ locale: string }>();

  return (
    <header className="relative p-[1.6rem] bg-primary block justify-center items-center">
      {/* AgrospAI icon */}
      <Link href="/" className="absolute left-2.5 top-[20px]">
        <Image src={logo} alt="AgrospAI logo" className="w-[15rem] h-[6rem]" />
      </Link>

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
        <div className="transition hover:scale-105">
          <LocalePicker />
        </div>
      </nav>
    </header>
  );
}

export default Header;
