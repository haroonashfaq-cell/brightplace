"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { projectsApi } from "@/lib/api-client";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export default function ProjectsPage() {
  const { data: projects, isLoading } = useQuery({
    queryKey: ["projects"],
    queryFn: () => projectsApi.list(),
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Projects</h1>
        <Link href="/projects/new">
          <Button>New Project</Button>
        </Link>
      </div>

      {isLoading ? (
        <div className="space-y-3">
          <Skeleton className="h-20 w-full" />
          <Skeleton className="h-20 w-full" />
        </div>
      ) : !projects || projects.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <p className="mb-4 text-gray-500">No projects yet</p>
            <Link href="/projects/new">
              <Button>Create Your First Project</Button>
            </Link>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {projects.map((project) => (
            <Link
              key={project.id}
              href={`/projects/${project.id}/keywords`}
              className="block"
            >
              <Card className="transition-colors hover:bg-gray-50">
                <CardContent className="flex items-center justify-between py-4">
                  <div>
                    <p className="font-medium">{project.domain}</p>
                    {project.niche && (
                      <p className="text-sm text-gray-500">{project.niche}</p>
                    )}
                  </div>
                  <div className="text-sm text-gray-400">
                    {new Date(project.created_at).toLocaleDateString()}
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
