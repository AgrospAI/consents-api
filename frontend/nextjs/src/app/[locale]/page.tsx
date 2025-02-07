import Section from "@/components/Section";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { useTranslations } from "next-intl";

const contents = [
  {
    trigger: "content.first.title",
    content: "content.first.content",
  },
  {
    trigger: "content.second.title",
    content: "content.second.content",
  },
  {
    trigger: "content.third.title",
    content: "content.third.content",
  },
];

function HomePage() {
  const t = useTranslations("HomePage");

  return (
    <Section className="pt-8">
      <div className="my-4">
        <h1 className="font-bold text-xl">{t("title")}</h1>
        <p>{t("description")}</p>
      </div>

      <Accordion type="single" collapsible defaultValue="item-0">
        {contents.map(({ trigger, content }, idx) => (
          <AccordionItem key={trigger} value={`item-${idx}`}>
            <AccordionTrigger>
              <p className="font-bold">{t(trigger)}</p>
            </AccordionTrigger>
            <AccordionContent>{t(content)}</AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </Section>
  );
}

export default HomePage;
