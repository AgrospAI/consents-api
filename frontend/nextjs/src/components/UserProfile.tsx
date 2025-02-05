import { Moon, UserCog } from "lucide-react";

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
    <a key={index} href={href}>
      {icon}
      <span>{name}</span>
    </a>
  );
}

function Settings() {
  return (
    <>
      {/* {settings.map((group, groupIdx) => (
        <h2>{group.name}</h2>

        group.settings.map((setting, settingIdx) => {

        });

      ))} */}
    </>
  );
}

export default Settings;
