import { getSupportedChains } from "./chains";
import { chainIdsSupported } from "@/configs/app.config";

export function accountTruncate(
  account: string,
  begin: number = 6,
  end: number = 38
): string {
  if (!account || account === "") return "";
  const middle = account.substring(begin, end);
  const truncated = account.replace(middle, "…");
  return truncated; // for example 0xb9A3...941d
}

// Wagmi client
// export const wagmiClient = createClient(
//   getDefaultClient({
//     appName: "Pontus-X",
//     infuraId: process.env.NEXT_PUBLIC_INFURA_PROJECT_ID,
//     // TODO: mapping between appConfig.chainIdsSupported and wagmi chainId
//     chains: getSupportedChains(chainIdsSupported),
//     walletConnectProjectId: process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID,
//   })
// );

// ConnectKit CSS overrides
// https://docs.family.co/connectkit/theming#theme-variables
export const connectKitTheme = {
  "--ck-font-family": "var(--font-family-base)",
  "--ck-border-radius": "var(--border-radius)",
  "--ck-overlay-background": "var(--background-body-transparent)",
  "--ck-modal-box-shadow": "0 0 20px 20px var(--box-shadow-color)",
  "--ck-body-background": "var(--background-body)",
  "--ck-body-color": "var(--font-color-text)",
  "--ck-primary-button-border-radius": "var(--border-radius)",
  "--ck-primary-button-color": "var(--font-color-heading)",
  "--ck-primary-button-background": "var(--background-content)",
  "--ck-secondary-button-border-radius": "var(--border-radius)",
};
