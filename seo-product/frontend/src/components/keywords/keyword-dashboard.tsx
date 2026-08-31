"use client";

import { useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { useKeywords } from "@/hooks/use-keywords";
import { keywordsApi, projectsApi } from "@/lib/api-client";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { KeywordFilterBar } from "./keyword-filters";
import { KeywordTable } from "./keyword-table";
import { SelectedKeywordsSidebar } from "./selected-keywords-sidebar";
import { CsvImport } from "./csv-import";
import { FIXED_TABS, getCategoryTabs } from "@/types/keyword";
import { cn } from "@/lib/utils";

interface Props {
  projectId: string;
}

export function KeywordDashboard({ projectId }: Props) {
  const {
    items,
    totalGaps,
    page,
    pageSize,
    totalPages,
    selectedKeywords,
    activeTab,
    isLoading,
    isRefreshing,
    filters,
    updateFilters,
    changeTab,
    refresh,
    selectKeyword,
    removeSelected,
  } = useKeywords(projectId);

  const [showImport, setShowImport] = useState(false);

  // Get project niche for category tabs
  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => projectsApi.get(projectId),
    enabled: !!projectId,
  });

  // Get category counts from DB
  const { data: categories } = useQuery({
    queryKey: ["keyword-categories", projectId],
    queryFn: () => keywordsApi.getCategories(projectId),
    enabled: !!projectId,
  });

  const categoryCountMap = new Map(
    (categories || []).map((c) => [c.category, c.count])
  );

  // Get niche-specific tabs
  const nicheTabs = getCategoryTabs(project?.niche || null);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Keyword Universe</h1>
          {project && (
            <p className="text-sm text-gray-500">
              {project.domain} — {project.niche || "General"}
            </p>
          )}
        </div>
        <div className="flex gap-2">
          <Link href={`/projects/${projectId}/settings`}>
            <Button variant="outline" size="sm">
              <svg className="mr-1.5 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Settings
            </Button>
          </Link>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowImport(true)}
          >
            <svg className="mr-1.5 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Import CSV
          </Button>
          <Button
            onClick={() => refresh()}
            disabled={isRefreshing}
            size="sm"
          >
            {isRefreshing ? "Refreshing..." : "Refresh Data"}
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid gap-3 md:grid-cols-4">
        <Card>
          <CardContent className="py-4">
            <p className="text-xs text-gray-500">Total Keywords</p>
            <p className="text-2xl font-bold">{totalGaps.toLocaleString()}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs text-gray-500">Easy Wins (KD 0-10)</p>
            <p className="text-2xl font-bold text-green-600">
              {items.filter((k) => k.kd <= 10).length}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs text-gray-500">Quick Wins (KD 0-15)</p>
            <p className="text-2xl font-bold text-blue-600">
              {items.filter((k) => k.kd <= 15).length}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs text-gray-500">Selected</p>
            <p className="text-2xl font-bold text-purple-600">
              {selectedKeywords.length}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Category Tabs */}
      <div className="flex flex-wrap gap-1 rounded-lg border bg-white p-1.5">
        {/* Fixed filter tabs */}
        {FIXED_TABS.map((tab) => (
          <button
            key={tab.value}
            onClick={() => changeTab(tab.value)}
            className={cn(
              "rounded-md px-3 py-1.5 text-sm font-medium transition-colors",
              activeTab === tab.value
                ? "bg-gray-900 text-white"
                : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
            )}
          >
            {tab.label}
          </button>
        ))}

        {/* Divider */}
        <div className="mx-1 w-px self-stretch bg-gray-200" />

        {/* Niche-specific category tabs */}
        {nicheTabs.map((cat) => {
          const count = categoryCountMap.get(cat) || 0;
          return (
            <button
              key={cat}
              onClick={() => changeTab(cat)}
              className={cn(
                "rounded-md px-3 py-1.5 text-sm font-medium transition-colors",
                activeTab === cat
                  ? "bg-gray-900 text-white"
                  : "text-gray-600 hover:bg-gray-100 hover:text-gray-900",
                count === 0 && "opacity-40"
              )}
            >
              {cat}
              {count > 0 && (
                <span className="ml-1 text-xs opacity-60">({count})</span>
              )}
            </button>
          );
        })}
      </div>

      {/* Filters */}
      <KeywordFilterBar filters={filters} onUpdate={updateFilters} />

      {/* Main content */}
      <div className="grid gap-4 lg:grid-cols-[1fr_280px]">
        <KeywordTable
          projectId={projectId}
          items={items}
          isLoading={isLoading}
          page={page}
          totalPages={totalPages}
          totalGaps={totalGaps}
          pageSize={pageSize}
          filters={filters}
          onUpdateFilters={updateFilters}
          onSelect={selectKeyword}
        />

        <SelectedKeywordsSidebar
          projectId={projectId}
          keywords={selectedKeywords}
          onRemove={removeSelected}
        />
      </div>

      <CsvImport
        projectId={projectId}
        open={showImport}
        onClose={() => setShowImport(false)}
      />
    </div>
  );
}
