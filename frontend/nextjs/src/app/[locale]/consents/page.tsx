import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useTranslations } from "next-intl";
import React from "react";
import ConsentsTable from "@/components/consents/ConsentsTable";
import Consent, { statuses } from "@/utils/entities/Consent";

async function getData(): Promise<Consent[]> {
  const data = [
    {
      id: "1",
      name: "Consent 1",
      description: "Description for consent 1",
      status: "pending" as "pending",
    },
    {
      id: "2",
      name: "Consent 2",
      description: "Description for consent 2",
      status: "accepted" as "accepted",
    },
  ];

  for (let i = 3; i < 15; i++) {
    data.push({
      id: i.toString(),
      name: `Consent ${i}`,
      description: `Description for consent ${i}`,
      status: "pending",
    });
  }

  return data;
}

function ConsentsPage() {
  const t = useTranslations("Consents");

  return (
    <Tabs defaultValue="pending" className="size-full gap-y-0">
      <TabsList className="flex flex-row gap-x-4 bg-secondary text-white shadow-xl w-fit mx-auto">
        {statuses.map((status, idx) => (
          <TabsTrigger
            key={`trigger-${idx}`}
            value={status}
            className="hover:scale-105 hover:underline data-[state=active]:underline data-[state=active]:scale-105 data-[state=active]:font-bold data-[state=active]:text-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none"
          >
            {t(`tabs.${status}`)}
          </TabsTrigger>
        ))}
      </TabsList>
      {statuses.map((status, idx) => (
        <TabsContent
          key={`content-${idx}`}
          value={status}
          className="border border-gray-300 p-2 rounded-md shadow-md"
        >
          <ConsentsTable
            dataPromise={getData().then((x) =>
              x.filter((s) => s.status == status)
            )}
          />
        </TabsContent>
      ))}
    </Tabs>
  );
}

export default ConsentsPage;
