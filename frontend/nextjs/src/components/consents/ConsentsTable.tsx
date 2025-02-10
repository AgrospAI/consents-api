import React, { use } from "react";
import { DataTable } from "./DataTable";
import Consent from "@/utils/entities/Consent";
import { columns } from "./Columns";

interface Properties {
  dataPromise: Promise<Consent[]>;
}

function ConsentsTable({ dataPromise }: Readonly<Properties>) {
  const data = use(dataPromise);

  return <DataTable columns={columns} data={data} />;
}

export default ConsentsTable;
