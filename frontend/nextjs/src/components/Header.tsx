"use client";
import Image from "next/image";
import logo from "@public/logo-horizontal.svg";
import { Link } from "@/i18n/routing";
import LocalePicker from "@/components/LocalePicker";
import Navigation from "@/components/Navigation";
import ConnectWallet from "@/components/wallet/ConnectWallet";

function Header() {
  return (
    <header className="relative p-[1.6rem] bg-primary justify-center items-center flex flex-row gap-x-16">
      {/* AgrospAI icon */}
      <Link href="/" className="absolute left-2.5 top-[20px]">
        <Image src={logo} alt="AgrospAI logo" className="w-[15rem] h-[6rem]" />
      </Link>
      <Navigation>
        <div className="transition hover:scale-105 z-40">
          <LocalePicker />
        </div>
      </Navigation>
      <ConnectWallet />
    </header>
  );
}

export default Header;
