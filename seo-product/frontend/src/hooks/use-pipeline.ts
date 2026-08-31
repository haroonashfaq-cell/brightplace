"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { pipelineApi } from "@/lib/api-client";

export function usePipeline(projectId: string, keywordId: string) {
  const queryClient = useQueryClient();
  const queryKey = ["pipeline", projectId, keywordId];

  const statusQuery = useQuery({
    queryKey,
    queryFn: () => pipelineApi.getStatus(projectId, keywordId),
    enabled: !!projectId && !!keywordId,
    refetchInterval: (query) => {
      // Poll every 3s while any step is running
      const data = query.state.data;
      if (!data?.steps) return false;
      const hasRunning = Object.values(data.steps).some(
        (job) => job && job.status === "running"
      );
      return hasRunning ? 3000 : false;
    },
  });

  const researchMutation = useMutation({
    mutationFn: () => pipelineApi.startResearch(projectId, keywordId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey });
    },
  });

  const briefMutation = useMutation({
    mutationFn: () => pipelineApi.generateBrief(projectId, keywordId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey });
    },
  });

  const approveBriefMutation = useMutation({
    mutationFn: (briefId: string) =>
      pipelineApi.approveBrief(projectId, briefId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey });
    },
  });

  const writeMutation = useMutation({
    mutationFn: (briefId: string) =>
      pipelineApi.writeArticle(projectId, briefId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey });
    },
  });

  const qaMutation = useMutation({
    mutationFn: (articleId: string) => pipelineApi.runQa(projectId, articleId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey });
    },
  });

  const rewriteMutation = useMutation({
    mutationFn: (articleId: string) =>
      pipelineApi.rewriteFromQa(projectId, articleId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey });
    },
  });

  const status = statusQuery.data;
  const isAnyRunning = Object.values(status?.steps ?? {}).some(
    (job) => job && job.status === "running"
  );

  return {
    status,
    isLoading: statusQuery.isLoading,
    isAnyRunning,

    startResearch: researchMutation.mutate,
    isResearching: researchMutation.isPending,

    generateBrief: briefMutation.mutate,
    isGeneratingBrief: briefMutation.isPending,

    approveBrief: approveBriefMutation.mutate,
    isApprovingBrief: approveBriefMutation.isPending,

    writeArticle: writeMutation.mutate,
    isWriting: writeMutation.isPending,

    runQa: qaMutation.mutate,
    isRunningQa: qaMutation.isPending,

    rewriteFromQa: rewriteMutation.mutate,
    isRewriting: rewriteMutation.isPending,

    refetch: statusQuery.refetch,
  };
}
