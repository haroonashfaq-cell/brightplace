"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { pipelineApi } from "@/lib/api-client";
import type { Article, QaReport } from "@/types/pipeline";

interface Props {
  projectId: string;
  article: Article | null;
  briefId: string | null;
  briefStatus: string | null;
  onWriteArticle: (briefId: string) => void;
  isWriting: boolean;
  onRunQa: (articleId: string) => void;
  isRunningQa: boolean;
  onRewriteFromQa?: (articleId: string) => void;
  isRewriting?: boolean;
}

export function ArticleView({
  projectId,
  article,
  briefId,
  briefStatus,
  onWriteArticle,
  isWriting,
  onRunQa,
  isRunningQa,
  onRewriteFromQa,
  isRewriting,
}: Props) {
  if (!article) {
    const canWrite = briefId && (briefStatus === "approved" || briefStatus === "completed");
    return (
      <Card>
        <CardContent className="flex flex-col items-center py-12">
          <svg className="mb-4 h-12 w-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          <p className="mb-4 text-gray-500">
            {canWrite
              ? "Write the full article from the approved brief"
              : "Approve the brief first to start writing"}
          </p>
          <Button
            onClick={() => briefId && onWriteArticle(briefId)}
            disabled={isWriting || !canWrite}
          >
            {isWriting ? "Writing..." : "Write Article"}
          </Button>
        </CardContent>
      </Card>
    );
  }

  const qaReport = article.qa_report as QaReport | undefined;
  const hasQa = qaReport && "checks" in qaReport;

  const handleExport = async (format: "md" | "html") => {
    try {
      const { blob, filename } = await pipelineApi.exportArticle(
        projectId,
        article.id,
        format
      );
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      // Export failed silently
    }
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Badge
            className={
              article.status === "qa_passed"
                ? "bg-green-100 text-green-800"
                : article.status === "published"
                  ? "bg-blue-100 text-blue-800"
                  : "bg-yellow-100 text-yellow-800"
            }
          >
            {article.status}
          </Badge>
          <span className="text-sm text-gray-500">
            {article.word_count.toLocaleString()} words
          </span>
          {article.seo_score > 0 && (
            <span className="text-sm text-gray-500">
              SEO Score: {article.seo_score}%
            </span>
          )}
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => onRunQa(article.id)}
            disabled={isRunningQa}
          >
            {isRunningQa ? "Running QA..." : "Run QA"}
          </Button>
          <Button variant="outline" size="sm" onClick={() => handleExport("md")}>
            Export MD
          </Button>
          <Button variant="outline" size="sm" onClick={() => handleExport("html")}>
            Export HTML
          </Button>
        </div>
      </div>

      {/* QA Report */}
      {hasQa && (
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-sm font-semibold">QA Report</h4>
              <Badge
                className={
                  qaReport.all_passed
                    ? "bg-green-100 text-green-800"
                    : "bg-red-100 text-red-800"
                }
              >
                {qaReport.passed}/{qaReport.total} passed
              </Badge>
            </div>
            <div className="space-y-2">
              {qaReport.checks.map((check, i) => (
                <div
                  key={i}
                  className={`rounded-md border p-3 ${
                    check.passed ? "border-green-200 bg-green-50" : "border-red-200 bg-red-50"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {check.passed ? (
                      <svg className="h-4 w-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      <svg className="h-4 w-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    )}
                    <p className="text-sm font-medium">{check.name}</p>
                  </div>
                  {check.issues.length > 0 && (
                    <div className="mt-2 space-y-1">
                      {check.issues.map((issue, j) => (
                        <p key={j} className="text-xs text-red-700">
                          {issue}
                        </p>
                      ))}
                    </div>
                  )}
                  {check.suggestions.length > 0 && (
                    <div className="mt-2 space-y-1">
                      {check.suggestions.map((sug, j) => (
                        <p key={j} className="text-xs text-gray-500">
                          Suggestion: {sug}
                        </p>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
            {!qaReport.all_passed && onRewriteFromQa && (
              <div className="mt-4 rounded-md border border-amber-200 bg-amber-50 p-3">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-amber-900">
                      {qaReport.total - qaReport.passed} check{qaReport.total - qaReport.passed > 1 ? "s" : ""} failed
                    </p>
                    <p className="text-xs text-amber-700">
                      Auto-fix all QA issues and re-run checks
                    </p>
                  </div>
                  <Button
                    onClick={() => onRewriteFromQa(article.id)}
                    disabled={isRewriting}
                    size="sm"
                  >
                    {isRewriting ? "Rewriting..." : "Fix & Rewrite"}
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Article Preview */}
      <Card>
        <CardContent className="pt-6">
          <h4 className="mb-3 text-sm font-semibold">Article Preview</h4>
          {article.content_html ? (
            <div
              className="prose prose-sm max-w-none"
              dangerouslySetInnerHTML={{ __html: article.content_html }}
            />
          ) : (
            <pre className="max-h-[600px] overflow-auto whitespace-pre-wrap rounded-md bg-gray-50 p-4 text-sm">
              {article.content_md}
            </pre>
          )}
        </CardContent>
      </Card>

      {/* Re-write */}
      <div className="flex gap-3">
        {briefId && (
          <Button
            variant="outline"
            onClick={() => onWriteArticle(briefId)}
            disabled={isWriting}
          >
            {isWriting ? "Rewriting..." : "Rewrite Article"}
          </Button>
        )}
      </div>
    </div>
  );
}
