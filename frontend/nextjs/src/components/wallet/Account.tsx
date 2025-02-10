"use client";
import { FormEvent } from "react";
import { accountTruncate } from "@/utils/wallet";
import { useAccount } from "wagmi";
import { useModal } from "connectkit";

// TODO : Generic LOADER

interface AccountProperties {
  ref: any;
}

function Account({ ref }: AccountProperties) {
  const { address, isConnecting, isDisconnected } = useAccount();
  const { setOpen } = useModal();

  async function handleActivation(e: FormEvent<HTMLButtonElement>) {
    // prevent accidentally submitting a form the button might be in
    e.preventDefault();

    setOpen(true);
  }

  if (isConnecting) {
    return <div>Connecting...</div>;
  }

  if (isDisconnected) {
    return <div>Disconnected</div>;
  }

  return address ? (
    <button aria-label="Account" ref={ref} onClick={(e) => e.preventDefault()}>
      <span title={address}>{accountTruncate(address)}</span>
    </button>
  ) : (
    <button
      onClick={(e) => handleActivation(e)}
      // Need the `ref` here although we do not want
      // the Tippy to show in this state.
      ref={ref}
    >
      Connect <span>Wallet</span>
    </button>
  );
}

export default Account;
