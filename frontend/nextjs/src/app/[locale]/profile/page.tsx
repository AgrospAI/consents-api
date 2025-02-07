"use client";
import AuthAlert from "@/components/AuthAlert";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import useUser from "@/hooks/useUser";
import { CircleAlert, Moon, UserCog } from "lucide-react";
import Link from "next/link";

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

function Settings() {
  const user = useUser();

  return (
    <>
      {!user && <AuthAlert />}

      <h2>Welcome: {user?.public_key}</h2>
      <h1>Settings</h1>
    </>
  );
}

export default Settings;
