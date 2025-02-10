"use client";
import AuthAlert from "@/components/AuthAlert";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import useUser from "@/hooks/useUser";
import { CircleAlert, Moon, UserCog } from "lucide-react";
import { useTranslations } from "next-intl";
import Link from "next/link";
import { useAccount } from "wagmi";

interface Settings {
  name: string;
  href: string;
  icon: any;
}

interface SettingsGroup {
  name: string;
  settings: Settings[];
}

const account: Settings[] = [
  {
    name: "Edit Profile",
    href: "/settings/edit-profile",
    icon: UserCog,
  },
];

const customization: Settings[] = [
  {
    name: "Theme",
    href: "/settings/theme",
    icon: Moon,
  },
];

const settings: SettingsGroup[] = [
  { name: "Account", settings: account },
  { name: "Customization", settings: customization },
];

function IndividualSetting({ name, href, icon }: Settings, index: number) {
  return (
    <Link href={href}>
      {icon} {name}
    </Link>
  );
}

function WalletSettings() {
  const t = useTranslations("Account");
  const { address, isConnecting, isDisconnected } = useAccount();

  if (isDisconnected)
    return <AuthAlert variant="destructive" message={t("NotConnected")} />;

  if (isConnecting)
    return <AuthAlert variant="default" message={t("Connecting")} />;

  return (
    <>
      <h1>Settings: {address}</h1>
    </>
  );
}

export default WalletSettings;
