"use client";

import { useState } from "react";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { usePipeline } from "@/hooks/use-pipeline";
import { projectsApi, pipelineApi } from "@/lib/api-client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { PipelineSteps } from "./pipeline-steps";
import { ResearchView } from "./research-view";
import { BriefEditor } from "./brief-editor";
import { ArticleView } from "./article-view";
import { GuidelinesPanel } from "./guidelines-panel";
import type { PipelineStep } from "@/types/pipeline";

type ActiveView = PipelineStep | "guidelines";

interface Props {
  projectId: string;
  keywordId: string;
}

export function PipelineDashboard({ projectId, keywordId }: Props) {
  const [activeStep, setActiveStep] = useState<ActiveView>("research");
  const [sitemapInput, setSitemapInput] = useState("");
  const [showSitemap, setShowSitemap] = useState(false);
  const queryClient = useQueryClient();

  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => projectsApi.get(projectId),
    enabled: !!projectId,
  });

  const { data: sitemapData } = useQuery({
    queryKey: ["sitemap", projectId],
    queryFn: () => pipelineApi.getSitemap(projectId),
    enabled: !!projectId,
  });

  const sitemapMutation = useMutation({
    mutationFn: (url: string) => pipelineApi.saveSitemap(projectId, url),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["sitemap", projectId] });
      setSitemapInput("");
    },
  });

  const {
    status,
    isLoading,
    startResearch,
    isResearching,
    generateBrief,
    isGeneratingBrief,
    approveBrief,
    isApprovingBrief,
    writeArticle,
    isWriting,
    runQa,
    isRunningQa,
    rewriteFromQa,
    isRewriting,
  } = usePipeline(projectId, keywordId);

  if (isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-12 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  const hasSitemap = (sitemapData?.count ?? 0) > 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 text-sm text-gray-500 mb-1">
            <Link
              href={`/projects/${projectId}/keywords`}
              className="hover:text-gray-700"
            >
              Keywords
            </Link>
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
            <span>Pipeline</span>
          </div>
          <h1 className="text-2xl font-bold">
            {status?.keyword || "Loading..."}
          </h1>
          {project && (
            <p className="text-sm text-gray-500">
              {project.domain} — {project.niche || "General"}
            </p>
          )}
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant={activeStep === "guidelines" ? "default" : "outline"}
            size="sm"
            onClick={() => setActiveStep(activeStep === "guidelines" ? "research" : "guidelines")}
          >
            <svg className="mr-1.5 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Guidelines
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowSitemap(!showSitemap)}
          >
            <svg className="mr-1.5 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
            Sitemap {hasSitemap && <Badge variant="secondary" className="ml-1">{sitemapData?.count}</Badge>}
          </Button>
          <Link href={`/projects/${projectId}/keywords`}>
            <Button variant="outline" size="sm">
              Back to Keywords
            </Button>
          </Link>
        </div>
      </div>

      {/* Sitemap Config */}
      {showSitemap && (
        <Card>
          <CardContent className="pt-6">
            <h4 className="mb-2 text-sm font-semibold">Sitemap for Internal Linking</h4>
            <p className="mb-3 text-xs text-gray-500">
              Add your sitemap URL so the writing agent can use real internal links instead of placeholders.
            </p>
            <div className="flex gap-2">
              <Input
                placeholder="https://yoursite.com/sitemap.xml"
                value={sitemapInput}
                onChange={(e) => setSitemapInput(e.target.value)}
                className="flex-1"
              />
              <Button
                onClick={() => sitemapMutation.mutate(sitemapInput)}
                disabled={!sitemapInput || sitemapMutation.isPending}
                size="sm"
              >
                {sitemapMutation.isPending ? "Fetching..." : "Save & Fetch"}
              </Button>
            </div>
            {hasSitemap && (
              <p className="mt-2 text-xs text-green-600">
                {sitemapData?.count} URLs loaded from sitemap
              </p>
            )}
          </CardContent>
        </Card>
      )}

      {/* Sitemap warning if not configured */}
      {!hasSitemap && !showSitemap && (
        <div
          className="flex items-center gap-2 rounded-md border border-amber-200 bg-amber-50 px-4 py-2 text-sm text-amber-800 cursor-pointer"
          onClick={() => setShowSitemap(true)}
        >
          <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          No sitemap configured. Click to add one for better internal linking.
        </div>
      )}

      {/* Pipeline Steps */}
      {activeStep !== "guidelines" && (
        <PipelineSteps
          steps={status?.steps || {}}
          activeStep={activeStep}
          onStepClick={(step) => setActiveStep(step as ActiveView)}
        />
      )}

      {/* Active Step Content */}
      <div>
        {activeStep === "guidelines" && (
          <GuidelinesPanel projectId={projectId} />
        )}

        {activeStep === "research" && (
          <ResearchView
            report={status?.research_report || null}
            onStartResearch={() => startResearch()}
            onGenerateBrief={() => {
              generateBrief();
              setActiveStep("brief");
            }}
            isResearching={isResearching}
            isGeneratingBrief={isGeneratingBrief}
            hasBrief={!!status?.brief}
          />
        )}

        {activeStep === "brief" && (
          <BriefEditor
            projectId={projectId}
            keywordId={keywordId}
            brief={status?.brief || null}
            onGenerateBrief={() => generateBrief()}
            isGeneratingBrief={isGeneratingBrief}
            hasResearch={status?.research_report?.status === "completed"}
            onApproveBrief={(briefId) => approveBrief(briefId)}
            isApprovingBrief={isApprovingBrief}
          />
        )}

        {activeStep === "write" && (
          <ArticleView
            projectId={projectId}
            article={status?.article || null}
            briefId={status?.brief?.id || null}
            briefStatus={status?.brief?.status || null}
            onWriteArticle={(briefId) => writeArticle(briefId)}
            isWriting={isWriting}
            onRunQa={(articleId) => {
              runQa(articleId);
              setActiveStep("qa");
            }}
            isRunningQa={isRunningQa}
            onRewriteFromQa={(articleId) => rewriteFromQa(articleId)}
            isRewriting={isRewriting}
          />
        )}

        {activeStep === "qa" && (
          <ArticleView
            projectId={projectId}
            article={status?.article || null}
            briefId={status?.brief?.id || null}
            briefStatus={status?.brief?.status || null}
            onWriteArticle={(briefId) => writeArticle(briefId)}
            isWriting={isWriting}
            onRunQa={(articleId) => runQa(articleId)}
            isRunningQa={isRunningQa}
            onRewriteFromQa={(articleId) => rewriteFromQa(articleId)}
            isRewriting={isRewriting}
          />
        )}
      </div>
    </div>
  );
}
