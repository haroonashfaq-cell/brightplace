"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import type { SelectedKeyword } from "@/types/keyword";

interface Props {
  projectId: string;
  keywords: SelectedKeyword[];
  onRemove: (id: string) => void;
}

const STATUS_COLORS: Record<string, string> = {
  queued: "bg-gray-100 text-gray-700",
  researched: "bg-blue-100 text-blue-700",
  written: "bg-purple-100 text-purple-700",
  qa_passed: "bg-green-100 text-green-700",
};

export function SelectedKeywordsSidebar({ projectId, keywords, onRemove }: Props) {
  return (
    <div className="rounded-lg border bg-white">
      <div className="border-b px-4 py-3">
        <h3 className="font-medium">Selected ({keywords.length})</h3>
      </div>

      {keywords.length === 0 ? (
        <div className="px-4 py-8 text-center text-sm text-gray-400">
          Select keywords from the table to add them here
        </div>
      ) : (
        <div className="max-h-[calc(100vh-20rem)] divide-y overflow-y-auto">
          {keywords.map((kw) => (
            <div key={kw.id} className="px-4 py-3">
              <div className="flex items-start justify-between">
                <Link
                  href={`/projects/${projectId}/keywords/${kw.id}/pipeline`}
                  className="text-sm font-medium hover:text-blue-600"
                >
                  {kw.keyword}
                </Link>
                {kw.status !== "queued" && (
                  <Badge className={`ml-1 text-[10px] ${STATUS_COLORS[kw.status] || ""}`}>
                    {kw.status}
                  </Badge>
                )}
              </div>
              <div className="mt-1 text-xs text-gray-500">
                Vol: {kw.volume.toLocaleString()} | KD: {kw.kd}
              </div>
              <div className="mt-2 flex items-center gap-2">
                <Link href={`/projects/${projectId}/keywords/${kw.id}/pipeline`}>
                  <Button size="sm" className="h-7 text-xs">
                    Open Pipeline
                  </Button>
                </Link>
                <Button
                  size="sm"
                  variant="ghost"
                  className="h-7 text-xs text-red-500 hover:text-red-700"
                  onClick={() => onRemove(kw.id)}
                >
                  Remove
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}

      {keywords.length > 0 && (
        <div className="border-t p-4">
          <Link href={`/projects/${projectId}/keywords/${keywords[0].id}/pipeline`}>
            <Button className="w-full">
              Research & Write
            </Button>
          </Link>
          <p className="mt-1 text-center text-xs text-gray-400">
            Opens pipeline for first selected keyword
          </p>
        </div>
      )}
    </div>
  );
}
