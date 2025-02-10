export const statuses = ["accepted", "rejected", "pending"] as const;
export type Status = (typeof statuses)[number];

interface Consent {
  id: string;
  name: string;
  description: string;
  status: Status;
}

export default Consent;
