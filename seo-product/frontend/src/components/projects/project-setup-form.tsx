"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { projectsApi } from "@/lib/api-client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { Competitor } from "@/types/project";

export function ProjectSetupForm() {
  const router = useRouter();
  const [domain, setDomain] = useState("");
  const [niche, setNiche] = useState("");
  const [competitorInput, setCompetitorInput] = useState("");
  const [competitors, setCompetitors] = useState<
    { domain: string; auto: boolean }[]
  >([]);
  const [projectId, setProjectId] = useState<string | null>(null);
  const [step, setStep] = useState<"info" | "competitors">("info");

  const createProject = useMutation({
    mutationFn: () => projectsApi.create({ domain, niche: niche || undefined }),
    onSuccess: (project) => {
      setProjectId(project.id);
      setStep("competitors");
    },
  });

  const detectCompetitors = useMutation({
    mutationFn: () => projectsApi.detectCompetitors(projectId!),
    onSuccess: (data: Competitor[]) => {
      setCompetitors(data.map((c) => ({ domain: c.domain, auto: true })));
    },
  });

  const addCompetitor = useMutation({
    mutationFn: (compDomain: string) =>
      projectsApi.addCompetitor(projectId!, compDomain),
    onSuccess: (comp: Competitor) => {
      setCompetitors((prev) => [
        ...prev,
        { domain: comp.domain, auto: false },
      ]);
      setCompetitorInput("");
    },
  });

  function handleAddCompetitor(e: React.FormEvent) {
    e.preventDefault();
    if (competitorInput.trim()) {
      addCompetitor.mutate(competitorInput.trim());
    }
  }

  function handleContinue() {
    if (projectId) {
      router.push(`/projects/${projectId}/keywords`);
    }
  }

  if (step === "info") {
    return (
      <Card className="mx-auto max-w-lg">
        <CardHeader>
          <CardTitle>Set Up Your Project</CardTitle>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              createProject.mutate();
            }}
            className="space-y-4"
          >
            <div>
              <label className="text-sm font-medium" htmlFor="domain">
                Your website URL
              </label>
              <Input
                id="domain"
                value={domain}
                onChange={(e) => setDomain(e.target.value)}
                placeholder="https://www.example.com"
                required
              />
            </div>
            <div>
              <label className="text-sm font-medium" htmlFor="niche">
                Your niche / industry
              </label>
              <Input
                id="niche"
                value={niche}
                onChange={(e) => setNiche(e.target.value)}
                placeholder="e.g. Apartment rentals & renter education"
              />
            </div>
            <Button
              type="submit"
              className="w-full"
              disabled={!domain || createProject.isPending}
            >
              {createProject.isPending ? "Creating..." : "Continue"}
            </Button>
            {createProject.isError && (
              <p className="text-sm text-red-600">
                {createProject.error.message}
              </p>
            )}
          </form>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="mx-auto max-w-lg">
      <CardHeader>
        <CardTitle>Add Competitors</CardTitle>
        <p className="text-sm text-gray-500">
          Domain: <strong>{domain}</strong>
        </p>
      </CardHeader>
      <CardContent className="space-y-4">
        <Button
          variant="outline"
          className="w-full"
          onClick={() => detectCompetitors.mutate()}
          disabled={detectCompetitors.isPending}
        >
          {detectCompetitors.isPending
            ? "Detecting..."
            : "Auto-Detect Competitors"}
        </Button>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-white px-2 text-gray-500">
              or add manually
            </span>
          </div>
        </div>

        <form onSubmit={handleAddCompetitor} className="flex gap-2">
          <Input
            value={competitorInput}
            onChange={(e) => setCompetitorInput(e.target.value)}
            placeholder="competitor.com"
          />
          <Button
            type="submit"
            variant="outline"
            disabled={!competitorInput || addCompetitor.isPending}
          >
            Add
          </Button>
        </form>

        {competitors.length > 0 && (
          <div className="space-y-2">
            <p className="text-sm font-medium">
              Competitors ({competitors.length})
            </p>
            {competitors.map((c, i) => (
              <div
                key={i}
                className="flex items-center justify-between rounded-md border px-3 py-2 text-sm"
              >
                <span>{c.domain}</span>
                {c.auto && (
                  <span className="text-xs text-gray-400">auto-detected</span>
                )}
              </div>
            ))}
          </div>
        )}

        <Button
          className="w-full"
          onClick={handleContinue}
          disabled={competitors.length === 0}
        >
          Continue to Keywords
        </Button>
      </CardContent>
    </Card>
  );
}
