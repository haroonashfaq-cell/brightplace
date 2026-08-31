"use client";

import { useQuery } from "@tanstack/react-query";
import { keywordsApi } from "@/lib/api-client";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import type { KeywordGap } from "@/types/keyword";

interface Props {
  projectId: string;
  gap: KeywordGap;
  onSelect: (gap: KeywordGap) => void;
}

export function LongTailPanel({ projectId, gap, onSelect }: Props) {
  const { data, isLoading } = useQuery({
    queryKey: ["long-tail", projectId, gap.id],
    queryFn: () => keywordsApi.getLongTail(projectId, gap.id),
  });

  if (isLoading) {
    return (
      <tr>
        <td colSpan={5} className="px-4 py-3 bg-gray-50">
          <div className="space-y-2 pl-8">
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-2/3" />
            <Skeleton className="h-4 w-1/2" />
          </div>
        </td>
      </tr>
    );
  }

  if (!data || data.length === 0) {
    return (
      <tr>
        <td colSpan={5} className="px-4 py-3 bg-gray-50 text-sm text-gray-500">
          <div className="pl-8">No long-tail keywords found</div>
        </td>
      </tr>
    );
  }

  return (
    <>
      {data.map((lt) => (
        <tr key={lt.id} className="bg-gray-50 border-t border-gray-100">
          <td className="px-4 py-2 text-sm">
            <span className="pl-8 text-gray-600">{lt.keyword}</span>
          </td>
          <td className="px-4 py-2 text-sm text-right tabular-nums">
            {lt.volume.toLocaleString()}
          </td>
          <td className="px-4 py-2 text-sm text-right tabular-nums">
            {lt.kd}
          </td>
          <td className="px-4 py-2 text-sm">
            {lt.intent && (
              <Badge variant="outline" className="text-xs capitalize">
                {lt.intent}
              </Badge>
            )}
          </td>
          <td className="px-4 py-2 text-sm text-right">
            <Button
              size="sm"
              variant="ghost"
              className="text-xs"
              onClick={() =>
                onSelect({
                  ...gap,
                  keyword: lt.keyword,
                  volume: lt.volume,
                  kd: lt.kd,
                  intent: lt.intent,
                })
              }
            >
              Select
            </Button>
          </td>
        </tr>
      ))}
    </>
  );
}
