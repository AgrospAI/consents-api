import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin();

const nextConfig: import("next").NextConfig = {};

module.exports = withNextIntl(nextConfig);
