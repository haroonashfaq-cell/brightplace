"use client";

import { useState, useCallback } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { keywordsApi } from "@/lib/api-client";
import type { KeywordFilters, KeywordGap } from "@/types/keyword";

export function useKeywords(projectId: string) {
  const queryClient = useQueryClient();
  const [filters, setFilters] = useState<KeywordFilters>({
    page: 1,
    page_size: 20,
    sort_by: "volume",
    sort_dir: "desc",
  });
  const [activeTab, setActiveTab] = useState("");

  // Build effective filters based on tab + manual filters
  const effectiveFilters: KeywordFilters = { ...filters };
  if (activeTab === "__easy_wins") {
    effectiveFilters.kd_max = 10;
    effectiveFilters.category = undefined;
  } else if (activeTab === "__quick_wins") {
    effectiveFilters.kd_max = 15;
    effectiveFilters.category = undefined;
  } else if (activeTab === "__long_tail") {
    // Long-tail gold: 4+ words, low KD
    effectiveFilters.kd_max = 20;
    effectiveFilters.category = undefined;
    // Note: is_long_tail filter handled server-side if needed
  } else if (activeTab) {
    effectiveFilters.category = activeTab;
  }

  const gapsQuery = useQuery({
    queryKey: ["keyword-gaps", projectId, effectiveFilters],
    queryFn: () => keywordsApi.getGaps(projectId, effectiveFilters),
    enabled: !!projectId,
  });

  const selectedQuery = useQuery({
    queryKey: ["selected-keywords", projectId],
    queryFn: () => keywordsApi.listSelected(projectId),
    enabled: !!projectId,
  });

  const refreshMutation = useMutation({
    mutationFn: () => keywordsApi.refreshGaps(projectId),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["keyword-gaps", projectId],
      });
    },
  });

  const selectMutation = useMutation({
    mutationFn: (gap: KeywordGap) =>
      keywordsApi.addSelected(projectId, {
        keyword: gap.keyword,
        volume: gap.volume,
        kd: gap.kd,
        intent: gap.intent,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["selected-keywords", projectId],
      });
    },
  });

  const removeMutation = useMutation({
    mutationFn: (keywordId: string) =>
      keywordsApi.deleteSelected(projectId, keywordId),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["selected-keywords", projectId],
      });
    },
  });

  const updateFilters = useCallback(
    (newFilters: Partial<KeywordFilters>) => {
      setFilters((prev) => ({ ...prev, ...newFilters, page: newFilters.page ?? 1 }));
    },
    []
  );

  const changeTab = useCallback((tab: string) => {
    setActiveTab(tab);
    setFilters((prev) => ({ ...prev, page: 1 }));
  }, []);

  const gaps = gapsQuery.data;
  const totalGaps = gaps?.total_count ?? 0;
  const items = gaps?.items ?? [];

  return {
    items,
    totalGaps,
    page: filters.page ?? 1,
    pageSize: filters.page_size ?? 20,
    totalPages: Math.ceil(totalGaps / (filters.page_size ?? 20)),
    selectedKeywords: selectedQuery.data ?? [],
    activeTab,

    isLoading: gapsQuery.isLoading,
    isRefreshing: refreshMutation.isPending,

    filters,
    updateFilters,
    changeTab,
    refresh: refreshMutation.mutate,
    selectKeyword: selectMutation.mutate,
    removeSelected: removeMutation.mutate,
  };
}
