"use client";

import { use } from "react";
import { PipelineDashboard } from "@/components/pipeline/pipeline-dashboard";

export default function PipelinePage({
  params,
}: {
  params: Promise<{ projectId: string; keywordId: string }>;
}) {
  const { projectId, keywordId } = use(params);

  return <PipelineDashboard projectId={projectId} keywordId={keywordId} />;
}
