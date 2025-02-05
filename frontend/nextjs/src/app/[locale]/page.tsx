import { useTranslations } from "next-intl";

function HomePage() {
  const t = useTranslations("HomePage");

  return (
    <>
      <h1>{t("title")}</h1>
      <p>{t("description")}</p>
    </>
  );
}

export default HomePage;
