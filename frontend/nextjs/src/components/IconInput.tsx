import React, { ReactNode } from "react";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

interface Properties {
  id: string;
  icon: ReactNode;
  placeholder: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

function IconInput({ id, icon, placeholder, onChange }: Properties) {
  return (
    <div className="relative w-full flex flex-row max-w-sm items-center align-middle gap-1.5">
      <Label
        htmlFor={id}
        className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 z-10"
      >
        {icon}
      </Label>
      <Input
        id={id}
        placeholder={placeholder}
        onChange={onChange}
        className="pl-10 max-w-sm"
      />
    </div>
  );
}

export default IconInput;
