"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { projectsApi } from "@/lib/api-client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import type { Competitor } from "@/types/project";

interface Props {
  projectId: string;
}

export function ProjectSettings({ projectId }: Props) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [competitorInput, setCompetitorInput] = useState("");
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const { data: project, isLoading: projectLoading } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => projectsApi.get(projectId),
  });

  const { data: competitors, isLoading: compsLoading } = useQuery({
    queryKey: ["competitors", projectId],
    queryFn: () => projectsApi.listCompetitors(projectId),
  });

  const detectMutation = useMutation({
    mutationFn: () => projectsApi.detectCompetitors(projectId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["competitors", projectId] });
    },
  });

  const addMutation = useMutation({
    mutationFn: (domain: string) =>
      projectsApi.addCompetitor(projectId, domain),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["competitors", projectId] });
      setCompetitorInput("");
    },
  });

  const deleteCompMutation = useMutation({
    mutationFn: (competitorId: string) =>
      projectsApi.deleteCompetitor(projectId, competitorId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["competitors", projectId] });
    },
  });

  const deleteProjectMutation = useMutation({
    mutationFn: () => projectsApi.delete(projectId),
    onSuccess: () => {
      router.push("/projects");
    },
  });

  function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    if (competitorInput.trim()) {
      addMutation.mutate(competitorInput.trim());
    }
  }

  if (projectLoading) {
    return <div className="text-gray-500">Loading...</div>;
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Project Settings</h1>
        <Button
          variant="outline"
          onClick={() => router.push(`/projects/${projectId}/keywords`)}
        >
          Back to Keywords
        </Button>
      </div>

      {/* Project Info */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Project Details</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div>
            <label className="text-sm font-medium text-gray-500">Domain</label>
            <p className="text-sm">{project?.domain}</p>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-500">Niche</label>
            <p className="text-sm">{project?.niche || "Not set"}</p>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-500">
              Created
            </label>
            <p className="text-sm">
              {project?.created_at
                ? new Date(project.created_at).toLocaleDateString()
                : "-"}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Competitors */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Competitors</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Auto-detect */}
          <Button
            variant="outline"
            className="w-full"
            onClick={() => detectMutation.mutate()}
            disabled={detectMutation.isPending}
          >
            {detectMutation.isPending
              ? "Detecting..."
              : "Auto-Detect Competitors"}
          </Button>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <Separator />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white px-2 text-gray-500">
                or add manually
              </span>
            </div>
          </div>

          {/* Manual add */}
          <form onSubmit={handleAdd} className="flex gap-2">
            <Input
              value={competitorInput}
              onChange={(e) => setCompetitorInput(e.target.value)}
              placeholder="competitor.com"
            />
            <Button
              type="submit"
              variant="outline"
              disabled={!competitorInput || addMutation.isPending}
            >
              {addMutation.isPending ? "Adding..." : "Add"}
            </Button>
          </form>

          {/* Competitor list */}
          {compsLoading ? (
            <p className="text-sm text-gray-400">Loading competitors...</p>
          ) : !competitors || competitors.length === 0 ? (
            <p className="text-sm text-gray-400">No competitors added yet</p>
          ) : (
            <div className="space-y-2">
              {competitors.map((comp: Competitor) => (
                <div
                  key={comp.id}
                  className="flex items-center justify-between rounded-md border px-3 py-2"
                >
                  <div>
                    <span className="text-sm font-medium">{comp.domain}</span>
                    {comp.auto_detected && (
                      <span className="ml-2 text-xs text-gray-400">
                        auto-detected
                      </span>
                    )}
                  </div>
                  <Button
                    size="sm"
                    variant="ghost"
                    className="h-7 text-xs text-red-500 hover:text-red-700"
                    onClick={() => deleteCompMutation.mutate(comp.id)}
                    disabled={deleteCompMutation.isPending}
                  >
                    Remove
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Danger Zone */}
      <Card className="border-red-200">
        <CardHeader>
          <CardTitle className="text-lg text-red-600">Danger Zone</CardTitle>
        </CardHeader>
        <CardContent>
          {!showDeleteConfirm ? (
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Delete this project</p>
                <p className="text-xs text-gray-500">
                  Permanently removes the project, all keywords, and competitors
                </p>
              </div>
              <Button
                variant="outline"
                className="border-red-300 text-red-600 hover:bg-red-50"
                onClick={() => setShowDeleteConfirm(true)}
              >
                Delete Project
              </Button>
            </div>
          ) : (
            <div className="space-y-3">
              <p className="text-sm text-red-600">
                Are you sure? This cannot be undone.
              </p>
              <div className="flex gap-2">
                <Button
                  variant="destructive"
                  onClick={() => deleteProjectMutation.mutate()}
                  disabled={deleteProjectMutation.isPending}
                >
                  {deleteProjectMutation.isPending
                    ? "Deleting..."
                    : "Yes, delete permanently"}
                </Button>
                <Button
                  variant="outline"
                  onClick={() => setShowDeleteConfirm(false)}
                >
                  Cancel
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
