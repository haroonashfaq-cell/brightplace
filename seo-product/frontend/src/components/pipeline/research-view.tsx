"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { ResearchReport } from "@/types/pipeline";

interface Props {
  report: ResearchReport | null;
  onStartResearch: () => void;
  onGenerateBrief: () => void;
  isResearching: boolean;
  isGeneratingBrief: boolean;
  hasBrief: boolean;
}

type Section = "serp" | "paa" | "reddit";

export function ResearchView({
  report,
  onStartResearch,
  onGenerateBrief,
  isResearching,
  isGeneratingBrief,
  hasBrief,
}: Props) {
  const [expanded, setExpanded] = useState<Section | null>("serp");

  if (!report || report.status === "pending") {
    return (
      <Card>
        <CardContent className="flex flex-col items-center py-12">
          <svg className="mb-4 h-12 w-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <p className="mb-4 text-gray-500">
            Run research to analyze SERP, PAA questions, and Reddit insights
          </p>
          <Button onClick={onStartResearch} disabled={isResearching}>
            {isResearching ? "Researching..." : "Start Research"}
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (report.status === "running") {
    return (
      <Card>
        <CardContent className="flex flex-col items-center py-12">
          <svg className="mb-4 h-12 w-12 animate-spin text-blue-500" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <p className="text-gray-600 font-medium">Researching...</p>
          <p className="mt-1 text-sm text-gray-400">
            Analyzing SERP results, PAA questions, and Reddit threads
          </p>
        </CardContent>
      </Card>
    );
  }

  if (report.status === "failed") {
    return (
      <Card>
        <CardContent className="flex flex-col items-center py-12">
          <p className="mb-4 text-red-500">Research failed. Please try again.</p>
          <Button onClick={onStartResearch} disabled={isResearching}>
            Retry Research
          </Button>
        </CardContent>
      </Card>
    );
  }

  const serp = report.serp_data;
  const paa = report.paa_data;
  const reddit = report.reddit_data;

  return (
    <div className="space-y-4">
      {/* SERP Analysis */}
      <Card>
        <button
          className="flex w-full items-center justify-between px-6 py-4 text-left"
          onClick={() => setExpanded(expanded === "serp" ? null : "serp")}
        >
          <div className="flex items-center gap-3">
            <h3 className="font-semibold">SERP Analysis</h3>
            <Badge variant="secondary">
              {serp?.organic_results?.length || 0} results
            </Badge>
          </div>
          <svg
            className={`h-5 w-5 transition-transform ${expanded === "serp" ? "rotate-180" : ""}`}
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        {expanded === "serp" && (
          <CardContent className="border-t pt-4">
            {serp?.featured_snippet && (
              <div className="mb-4 rounded-md border border-blue-200 bg-blue-50 p-3">
                <p className="text-xs font-medium text-blue-700 mb-1">Featured Snippet</p>
                <p className="text-sm">{serp.featured_snippet.description}</p>
                <p className="mt-1 text-xs text-blue-500">{serp.featured_snippet.url}</p>
              </div>
            )}
            <div className="space-y-3">
              {serp?.organic_results?.map((result, i) => (
                <div key={i} className="rounded-md border p-3">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-blue-700">{result.title}</p>
                      <p className="mt-0.5 text-xs text-green-700">{result.url}</p>
                      <p className="mt-1 text-xs text-gray-500">{result.description}</p>
                    </div>
                    <Badge variant="outline" className="ml-2 shrink-0">
                      #{result.position}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        )}
      </Card>

      {/* PAA Questions */}
      <Card>
        <button
          className="flex w-full items-center justify-between px-6 py-4 text-left"
          onClick={() => setExpanded(expanded === "paa" ? null : "paa")}
        >
          <div className="flex items-center gap-3">
            <h3 className="font-semibold">PAA Questions</h3>
            <Badge variant="secondary">
              {paa?.questions?.length || 0} questions
            </Badge>
          </div>
          <svg
            className={`h-5 w-5 transition-transform ${expanded === "paa" ? "rotate-180" : ""}`}
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        {expanded === "paa" && (
          <CardContent className="border-t pt-4">
            <div className="space-y-2">
              {paa?.questions?.map((q, i) => (
                <div key={i} className="flex items-start gap-3 rounded-md border p-3">
                  <div className="flex-1">
                    <p className="text-sm font-medium">{q.question}</p>
                  </div>
                  <div className="flex gap-1">
                    {q.gap && (
                      <Badge className="bg-amber-100 text-amber-800">Gap</Badge>
                    )}
                    <Badge variant="outline" className="capitalize">
                      {q.priority}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
            {paa?.additional_questions?.length > 0 && (
              <div className="mt-4">
                <p className="mb-2 text-sm font-medium text-gray-500">
                  Additional Questions (AI-suggested)
                </p>
                <div className="space-y-1">
                  {paa.additional_questions.map((q, i) => (
                    <p key={i} className="text-sm text-gray-600">
                      {q}
                    </p>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        )}
      </Card>

      {/* Reddit Insights */}
      <Card>
        <button
          className="flex w-full items-center justify-between px-6 py-4 text-left"
          onClick={() => setExpanded(expanded === "reddit" ? null : "reddit")}
        >
          <div className="flex items-center gap-3">
            <h3 className="font-semibold">Reddit Insights</h3>
            <Badge variant="secondary">
              {reddit?.thread_count || 0} threads
            </Badge>
          </div>
          <svg
            className={`h-5 w-5 transition-transform ${expanded === "reddit" ? "rotate-180" : ""}`}
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        {expanded === "reddit" && (
          <CardContent className="border-t pt-4">
            <div className="grid gap-4 md:grid-cols-2">
              <InsightList title="Pain Points" items={reddit?.pain_points} color="red" />
              <InsightList title="Real Numbers" items={reddit?.real_numbers} color="blue" />
              <InsightList title="Misconceptions" items={reddit?.misconceptions} color="amber" />
              <InsightList title="Practical Advice" items={reddit?.advice} color="green" />
            </div>
            {reddit?.common_questions?.length > 0 && (
              <div className="mt-4">
                <p className="mb-2 text-sm font-medium text-gray-500">Common Questions</p>
                <div className="space-y-1">
                  {reddit.common_questions.map((q, i) => (
                    <p key={i} className="text-sm text-gray-600">{q}</p>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        )}
      </Card>

      {/* Action */}
      <div className="flex gap-3">
        <Button variant="outline" onClick={onStartResearch} disabled={isResearching}>
          Re-run Research
        </Button>
        <Button onClick={onGenerateBrief} disabled={isGeneratingBrief || hasBrief}>
          {isGeneratingBrief ? "Generating Brief..." : hasBrief ? "Brief Generated" : "Generate Brief"}
        </Button>
      </div>
    </div>
  );
}

function InsightList({
  title,
  items,
  color,
}: {
  title: string;
  items: string[] | undefined;
  color: string;
}) {
  if (!items?.length) return null;

  const colorMap: Record<string, string> = {
    red: "border-red-200 bg-red-50",
    blue: "border-blue-200 bg-blue-50",
    amber: "border-amber-200 bg-amber-50",
    green: "border-green-200 bg-green-50",
  };

  return (
    <div className={`rounded-md border p-3 ${colorMap[color] || ""}`}>
      <p className="mb-2 text-xs font-semibold uppercase text-gray-500">
        {title}
      </p>
      <ul className="space-y-1">
        {items.map((item, i) => (
          <li key={i} className="text-sm text-gray-700">
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
