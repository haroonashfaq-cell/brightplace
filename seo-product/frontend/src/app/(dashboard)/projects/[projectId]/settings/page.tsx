"use client";

import { use } from "react";
import { ProjectSettings } from "@/components/projects/project-settings";

export default function ProjectSettingsPage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const { projectId } = use(params);

  return <ProjectSettings projectId={projectId} />;
}
