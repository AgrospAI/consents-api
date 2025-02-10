import { getDefaultConfig } from "connectkit";
import { type Chain } from "viem";
import { createConfig, http } from "wagmi";

declare module "wagmi" {
  interface Register {
    config: typeof config;
  }
}

export const pontusXDevnet: Chain = {
  id: 32456,
  name: "pontusx-devnet",
  nativeCurrency: {
    decimals: 18,
    name: "e-Euro",
    symbol: "eEUR",
  },
  rpcUrls: {
    default: { http: ["https://rpc.dev.pontus-x.eu"] },
  },
  testnet: true,
} as const satisfies Chain;

export const pontusXTestnet: Chain = {
  id: 32457,
  name: "pontusx-testnet",
  nativeCurrency: {
    decimals: 18,
    name: "e-Euro",
    symbol: "eEUR",
  },
  rpcUrls: {
    default: { http: ["https://rpc.test.pontus-x.eu"] },
  },
  testnet: true,
} as const satisfies Chain;

export const chains = [pontusXDevnet, pontusXTestnet];

export const config = createConfig(
  getDefaultConfig({
    chains: [pontusXDevnet, pontusXTestnet],
    transports: {
      [pontusXDevnet.id]: http(pontusXDevnet.rpcUrls.default.http[0]),
      [pontusXTestnet.id]: http(pontusXTestnet.rpcUrls.default.http[0]),
    },
    walletConnectProjectId: "asd",
    appName: "Pontus-X",
    appDescription:
      "Pontus-X is a decentralized exchange for the Polygon network.",
    appUrl: "https://agrospai.udl.cat",
    appIcon: "https://agrospai.udl.cat/favicon.ico",
  })
);

export const getSupportedChainIds = () => {
  return chains.map((c) => c.id);
};

// chain configs in ocean.js ConfigHelperConfig format
// see: https://github.com/oceanprotocol/ocean.js/blob/e07a7cb6ecea12b39ed96f994b4abe37806799a1/src/utils/ConfigHelper.ts#L8
// const chains = [
//   {
//     chainId: 32456,
//     isDefault: true,
//     isCustom: true,
//     network: "pontusx-devnet",
//     oceanTokenSymbol: "OCEAN",
//     oceanTokenAddress: "0xdF171F74a8d3f4e2A789A566Dce9Fa4945196112",
//     nftFactoryAddress: "0xFdC4a5DEaCDfc6D82F66e894539461a269900E13",
//     fixedRateExchangeAddress: "0x8372715D834d286c9aECE1AcD51Da5755B32D505",
//     dispenserAddress: "0x5461b629E01f72E0A468931A36e039Eea394f9eA",
//     opfCommunityFeeCollector: "0x1f84fB438292269219f9396D57431eA9257C23d4",
//     startBlock: 57428,
//     transactionBlockTimeout: 50,
//     transactionConfirmationBlocks: 1,
//     transactionPollingTimeout: 750,
//     gasFeeMultiplier: 1.1,
//     providerUri: "https://provider.agrospai.udl.cat",
//     providerAddress: "0x94549951623DD6c3265DBbB1b032d6cF48Ba7811",
//     metadataCacheUri: "https://aquarius.pontus-x.eu",
//     nodeUri: "https://rpc.dev.pontus-x.eu",
//     subgraphUri: "https://subgraph.dev.pontus-x.eu",
//     explorerUri: "https://explorer.pontus-x.eu/pontusx/dev",
//   },
//   {
//     chainId: 32457,
//     isDefault: true,
//     isCustom: true,
//     network: "pontusx-testnet",
//     oceanTokenSymbol: "OCEAN",
//     oceanTokenAddress: "0x5B190F9E2E721f8c811E4d584383E3d57b865C69",
//     nftFactoryAddress: "0x2C4d542ff791890D9290Eec89C9348A4891A6Fd2",
//     fixedRateExchangeAddress: "0xcE0F39abB6DA2aE4d072DA78FA0A711cBB62764E",
//     dispenserAddress: "0xaB5B68F88Bc881CAA427007559E9bbF8818026dE",
//     opfCommunityFeeCollector: "0xACC8d1B2a0007951fb4ed622ACB1C4fcCAbe778D",
//     startBlock: 82191,
//     transactionBlockTimeout: 50,
//     transactionConfirmationBlocks: 1,
//     transactionPollingTimeout: 750,
//     gasFeeMultiplier: 1.1,
//     providerUri: "https://provider.agrospai.udl.cat",
//     providerAddress: "0x94549951623DD6c3265DBbB1b032d6cF48Ba7811",
//     metadataCacheUri: "https://aquarius.pontus-x.eu",
//     nodeUri: "https://rpc.test.pontus-x.eu",
//     subgraphUri: "https://subgraph.test.pontus-x.eu",
//     explorerUri: "https://explorer.pontus-x.eu/pontusx/test",
//   },
// ];
