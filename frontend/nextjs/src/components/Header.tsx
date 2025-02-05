"use client";
import Image from "next/image";
import Link from "next/link";
import logo from "@public/logo-horizontal.svg";
import { Globe, TableOfContents, User } from "lucide-react";
import { ReactElement } from "react";

interface PageLink {
  href: string;
  label: string;
  icon: ReactElement;
}

const links: PageLink[] = [
  { href: "/", label: "Consents", icon: <TableOfContents /> },
  { href: "/profile", label: "Profile", icon: <User /> },
];

function Header() {
  return (
    <header className="relative p-[1.85rem] bg-primary block justify-center items-center">
      {/* AgrospAI icon */}
      <Link href="/" className="absolute left-2.5 top-[20px]">
        <Image src={logo} alt="AgrospAI logo" className="w-[15rem] h-[6rem]" />
      </Link>

      <nav className="flex px-3 text-sm justify-center items-center gap-x-8 font-bold text-secondary">
        {links.map(({ href, label, icon }, index) => (
          <Link
            key={index}
            aria-label={label}
            className="uppercase transition hover:underline underline-offset-4 flex items-center gap-x-2"
            href={href}
          >
            {icon} {label}
          </Link>
        ))}
        <Globe />
      </nav>
    </header>
  );
}

export default Header;
