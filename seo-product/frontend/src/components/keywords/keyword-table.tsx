"use client";

import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { LongTailPanel } from "./long-tail-panel";
import type { KeywordGap, KeywordFilters } from "@/types/keyword";
import { cn } from "@/lib/utils";

const difficultyColors: Record<string, string> = {
  "Very Easy": "bg-green-100 text-green-700",
  Easy: "bg-blue-100 text-blue-700",
  Moderate: "bg-yellow-100 text-yellow-700",
  Hard: "bg-red-100 text-red-700",
};

const tierColors: Record<string, string> = {
  T1: "bg-blue-100 text-blue-700",
  T2: "bg-gray-100 text-gray-600",
};

interface Props {
  projectId: string;
  items: KeywordGap[];
  isLoading: boolean;
  page: number;
  totalPages: number;
  totalGaps: number;
  pageSize: number;
  filters: KeywordFilters;
  onUpdateFilters: (f: Partial<KeywordFilters>) => void;
  onSelect: (gap: KeywordGap) => void;
}

export function KeywordTable({
  projectId,
  items,
  isLoading,
  page,
  totalPages,
  totalGaps,
  pageSize,
  filters,
  onUpdateFilters,
  onSelect,
}: Props) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  function handleSort(column: string) {
    const isCurrentSort = filters.sort_by === column;
    onUpdateFilters({
      sort_by: column,
      sort_dir: isCurrentSort && filters.sort_dir === "desc" ? "asc" : "desc",
      page,
    });
  }

  function sortIcon(column: string) {
    if (filters.sort_by !== column) return null;
    return <span className="ml-1">{filters.sort_dir === "desc" ? "↓" : "↑"}</span>;
  }

  if (isLoading) {
    return (
      <div className="space-y-2">
        {Array.from({ length: 8 }).map((_, i) => (
          <Skeleton key={i} className="h-10 w-full" />
        ))}
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="rounded-lg border bg-white py-12 text-center text-gray-500">
        No keywords found. Try adjusting filters or click Refresh Data.
      </div>
    );
  }

  return (
    <div className="rounded-lg border bg-white overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b bg-gray-50 text-left text-xs text-gray-500 uppercase tracking-wider">
            <th
              className="cursor-pointer px-3 py-2 font-medium hover:text-gray-900"
              onClick={() => handleSort("keyword")}
            >
              Keyword{sortIcon("keyword")}
            </th>
            <th
              className="cursor-pointer px-3 py-2 text-right font-medium hover:text-gray-900 whitespace-nowrap"
              onClick={() => handleSort("volume")}
            >
              Vol{sortIcon("volume")}
            </th>
            <th
              className="cursor-pointer px-3 py-2 text-right font-medium hover:text-gray-900"
              onClick={() => handleSort("kd")}
            >
              KD{sortIcon("kd")}
            </th>
            <th
              className="cursor-pointer px-3 py-2 text-right font-medium hover:text-gray-900"
              onClick={() => handleSort("cpc")}
            >
              CPC{sortIcon("cpc")}
            </th>
            <th className="px-3 py-2 font-medium">Difficulty</th>
            <th className="px-3 py-2 font-medium">Intent</th>
            <th className="px-3 py-2 font-medium">Category</th>
            <th className="px-3 py-2 font-medium">City</th>
            <th className="px-3 py-2 font-medium text-center">LT</th>
            <th className="px-3 py-2 font-medium">Tier</th>
            <th className="px-3 py-2 text-right font-medium">Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map((gap) => (
            <>
              <tr key={gap.id} className="border-t hover:bg-gray-50/50">
                <td className="px-3 py-2 font-medium max-w-[220px]">
                  <span className="block truncate" title={gap.keyword}>
                    {gap.keyword}
                  </span>
                </td>
                <td className="px-3 py-2 text-right tabular-nums whitespace-nowrap">
                  {gap.volume.toLocaleString()}
                </td>
                <td className="px-3 py-2 text-right tabular-nums">
                  <span
                    className={cn(
                      "font-medium",
                      gap.kd <= 10
                        ? "text-green-600"
                        : gap.kd <= 20
                          ? "text-blue-600"
                          : gap.kd <= 40
                            ? "text-yellow-600"
                            : "text-red-600"
                    )}
                  >
                    {gap.kd}
                  </span>
                </td>
                <td className="px-3 py-2 text-right tabular-nums text-gray-600">
                  {gap.cpc ? `$${gap.cpc.toFixed(2)}` : "-"}
                </td>
                <td className="px-3 py-2">
                  {gap.difficulty && (
                    <span
                      className={cn(
                        "inline-block rounded-full px-2 py-0.5 text-xs font-medium",
                        difficultyColors[gap.difficulty] || "bg-gray-100 text-gray-600"
                      )}
                    >
                      {gap.difficulty}
                    </span>
                  )}
                </td>
                <td className="px-3 py-2">
                  {gap.intent && gap.intent !== "unknown" && (
                    <Badge variant="outline" className="text-xs capitalize whitespace-nowrap">
                      {gap.intent}
                    </Badge>
                  )}
                </td>
                <td className="px-3 py-2 text-xs text-gray-600 whitespace-nowrap">
                  {gap.category || "-"}
                </td>
                <td className="px-3 py-2 text-xs text-gray-600 whitespace-nowrap">
                  {gap.city || "-"}
                </td>
                <td className="px-3 py-2 text-center">
                  {gap.is_long_tail ? (
                    <span className="text-green-600 text-xs font-medium">Yes</span>
                  ) : (
                    <span className="text-gray-400 text-xs">No</span>
                  )}
                </td>
                <td className="px-3 py-2">
                  {gap.tier && (
                    <span
                      className={cn(
                        "inline-block rounded px-1.5 py-0.5 text-xs font-medium",
                        tierColors[gap.tier] || "bg-gray-100 text-gray-600"
                      )}
                    >
                      {gap.tier}
                    </span>
                  )}
                </td>
                <td className="px-3 py-2 text-right whitespace-nowrap">
                  <div className="flex justify-end gap-1">
                    <Button
                      size="sm"
                      variant="ghost"
                      className="h-7 text-xs px-2"
                      onClick={() =>
                        setExpandedId(expandedId === gap.id ? null : gap.id)
                      }
                    >
                      {expandedId === gap.id ? "−" : "+"}
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      className="h-7 text-xs px-2"
                      onClick={() => onSelect(gap)}
                    >
                      Select
                    </Button>
                  </div>
                </td>
              </tr>
              {expandedId === gap.id && (
                <LongTailPanel
                  key={`lt-${gap.id}`}
                  projectId={projectId}
                  gap={gap}
                  onSelect={onSelect}
                />
              )}
            </>
          ))}
        </tbody>
      </table>

      {/* Pagination */}
      <div className="flex items-center justify-between border-t px-3 py-2 text-xs text-gray-500">
        <span>
          {(page - 1) * pageSize + 1}-{Math.min(page * pageSize, totalGaps)} of{" "}
          {totalGaps.toLocaleString()}
        </span>
        <div className="flex gap-1">
          <Button
            size="sm"
            variant="outline"
            className="h-7 text-xs"
            disabled={page <= 1}
            onClick={() => onUpdateFilters({ page: page - 1 })}
          >
            Prev
          </Button>
          <Button
            size="sm"
            variant="outline"
            className="h-7 text-xs"
            disabled={page >= totalPages}
            onClick={() => onUpdateFilters({ page: page + 1 })}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
