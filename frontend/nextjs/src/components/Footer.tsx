import { useTranslations } from "next-intl";

function Footer() {
  const t = useTranslations("Footer");

  return (
    <footer className="fixed left-0 bottom-0 w-full bg-footer flex justify-center items-center text-white py-8">
      <p>
        {t("developed")}{" "}
        <a
          className="text-primary hover:underline"
          href="https://agrospai.udl.cat"
          target="_blank"
        >
          AgrospAI
        </a>
        {", "}
        <a
          className="text-primary hover:underline"
          href="https://www.udl.cat"
          target="_blank"
        >
          {t("udl")}
        </a>
      </p>
    </footer>
  );
}

export default Footer;
