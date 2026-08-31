"use client";

import { use } from "react";
import { KeywordDashboard } from "@/components/keywords/keyword-dashboard";

export default function KeywordsPage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = use(params);

  return <KeywordDashboard projectId={projectId} />;
}
