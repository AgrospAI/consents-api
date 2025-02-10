import React from "react";
import { toDataUrl } from "myetherwallet-blockies";

interface AvatarProps {
  accountId: string;
  src?: string;
  className?: string;
}

function Avatar({ accountId, src, className }: AvatarProps) {
  return (
    <img
      className={`${className || ""}`}
      src={src || (accountId ? toDataUrl(accountId) : "")}
      alt="Avatar"
      aria-hidden="true"
    />
  );
}

export default Avatar;
