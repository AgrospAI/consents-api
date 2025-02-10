import { ConnectKitButton } from "connectkit";
import React from "react";
import { accountTruncate } from "@/utils/wallet";
import Avatar from "./Avatar";

function ConnectWallet() {
  return (
    <ConnectKitButton.Custom>
      {({ isConnected, isConnecting, show, hide, address, ensName, chain }) => {
        return (
          <button
            onClick={show}
            className="btn btn-primary bg-white text-primary-foreground border-border border-2 p-2"
          >
            {isConnected ? (
              <div className="flex flex-row gap-x-2 items-center">
                <Avatar accountId={address!} className="size-4 rounded-full" />
                {accountTruncate(address!)}
              </div>
            ) : (
              "Connect Wallet"
            )}
          </button>
        );
      }}
    </ConnectKitButton.Custom>
  );
}

export default ConnectWallet;
