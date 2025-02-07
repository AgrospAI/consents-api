import Image from "next/image";
import logo from "@public/logo-horizontal.svg";
import { Link } from "@/i18n/routing";
import LocalePicker from "@/components/LocalePicker";
import Navigation from "@/components/Navigation";

function Header() {
  return (
    <header className="relative p-[1.6rem] bg-primary justify-center items-center flex flex-row">
      {/* AgrospAI icon */}
      <Link href="/" className="absolute left-2.5 top-[20px]">
        <Image src={logo} alt="AgrospAI logo" className="w-[15rem] h-[6rem]" />
      </Link>
      <Navigation>
        <div className="transition hover:scale-105">
          <LocalePicker />
        </div>
      </Navigation>
      <p>aslñdjsalkd</p>
    </header>
  );
}

export default Header;
