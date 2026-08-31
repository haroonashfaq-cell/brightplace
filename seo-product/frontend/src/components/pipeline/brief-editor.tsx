"use client";

import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { pipelineApi } from "@/lib/api-client";
import type { Brief } from "@/types/pipeline";

interface Props {
  projectId: string;
  keywordId: string;
  brief: Brief | null;
  onGenerateBrief: () => void;
  isGeneratingBrief: boolean;
  hasResearch: boolean;
  onApproveBrief: (briefId: string) => void;
  isApprovingBrief: boolean;
}

export function BriefEditor({
  projectId,
  keywordId,
  brief,
  onGenerateBrief,
  isGeneratingBrief,
  hasResearch,
  onApproveBrief,
  isApprovingBrief,
}: Props) {
  const queryClient = useQueryClient();
  const [editingField, setEditingField] = useState<string | null>(null);
  const [editValue, setEditValue] = useState("");

  const updateMutation = useMutation({
    mutationFn: (data: Record<string, string>) =>
      pipelineApi.updateBrief(projectId, brief!.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["pipeline", projectId, keywordId],
      });
      setEditingField(null);
    },
  });

  if (!brief) {
    return (
      <Card>
        <CardContent className="flex flex-col items-center py-12">
          <svg className="mb-4 h-12 w-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p className="mb-4 text-gray-500">
            {hasResearch
              ? "Generate a content brief from your research data"
              : "Complete research first to generate a brief"}
          </p>
          <Button
            onClick={onGenerateBrief}
            disabled={isGeneratingBrief || !hasResearch}
          >
            {isGeneratingBrief ? "Generating..." : "Generate Brief"}
          </Button>
        </CardContent>
      </Card>
    );
  }

  const startEdit = (field: string, value: string) => {
    setEditingField(field);
    setEditValue(value || "");
  };

  const saveEdit = () => {
    if (editingField) {
      updateMutation.mutate({ [editingField]: editValue });
    }
  };

  const isEditable = brief.status === "draft";

  return (
    <div className="space-y-4">
      {/* Status */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Badge
            className={
              brief.status === "approved"
                ? "bg-green-100 text-green-800"
                : brief.status === "completed"
                  ? "bg-blue-100 text-blue-800"
                  : "bg-yellow-100 text-yellow-800"
            }
          >
            {brief.status}
          </Badge>
          <span className="text-sm text-gray-500">
            Target: {brief.word_count_target} words
          </span>
        </div>
        {isEditable && (
          <Button
            onClick={() => onApproveBrief(brief.id)}
            disabled={isApprovingBrief}
          >
            {isApprovingBrief ? "Approving..." : "Approve Brief"}
          </Button>
        )}
      </div>

      {/* Title & SEO */}
      <Card>
        <CardContent className="space-y-3 pt-6">
          <EditableField
            label="Title (H1)"
            value={brief.title || ""}
            field="title"
            editing={editingField}
            editValue={editValue}
            isEditable={isEditable}
            onStartEdit={startEdit}
            onSave={saveEdit}
            onCancel={() => setEditingField(null)}
            onChange={setEditValue}
          />
          <EditableField
            label="SEO Title"
            value={brief.seo_title || ""}
            field="seo_title"
            editing={editingField}
            editValue={editValue}
            isEditable={isEditable}
            onStartEdit={startEdit}
            onSave={saveEdit}
            onCancel={() => setEditingField(null)}
            onChange={setEditValue}
          />
          <EditableField
            label="Meta Description"
            value={brief.meta_description || ""}
            field="meta_description"
            editing={editingField}
            editValue={editValue}
            isEditable={isEditable}
            onStartEdit={startEdit}
            onSave={saveEdit}
            onCancel={() => setEditingField(null)}
            onChange={setEditValue}
          />
          <div>
            <span className="text-xs font-medium text-gray-500">Slug</span>
            <p className="text-sm">/resources/{brief.slug}</p>
          </div>
        </CardContent>
      </Card>

      {/* Snippet Paragraph */}
      {brief.snippet_paragraph && (
        <Card>
          <CardContent className="pt-6">
            <p className="mb-1 text-xs font-medium text-gray-500">
              Featured Snippet Paragraph ({brief.snippet_paragraph.split(/\s+/).length} words)
            </p>
            <p className="text-sm italic text-gray-700">{brief.snippet_paragraph}</p>
          </CardContent>
        </Card>
      )}

      {/* Outline */}
      <Card>
        <CardContent className="pt-6">
          <h4 className="mb-3 text-sm font-semibold">Content Outline</h4>
          <div className="space-y-2">
            {brief.outline?.map((section, i) => (
              <div
                key={i}
                className={`rounded-md border p-3 ${section.level === 3 ? "ml-6" : ""}`}
              >
                <p className="text-sm font-medium">
                  {"#".repeat(section.level)} {section.heading}
                </p>
                {section.instructions && (
                  <p className="mt-1 text-xs text-gray-500">
                    {section.instructions}
                  </p>
                )}
                {section.subsections?.map((sub, j) => (
                  <div key={j} className="ml-4 mt-2 rounded border-l-2 border-gray-200 pl-3">
                    <p className="text-sm font-medium">### {sub.heading}</p>
                    {sub.instructions && (
                      <p className="text-xs text-gray-500">{sub.instructions}</p>
                    )}
                  </div>
                ))}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Keywords */}
      <Card>
        <CardContent className="pt-6">
          <h4 className="mb-3 text-sm font-semibold">Target Keywords</h4>
          <div className="space-y-2">
            <div>
              <span className="text-xs text-gray-500">Primary: </span>
              <Badge>{brief.target_keywords?.primary}</Badge>
            </div>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs text-gray-500 self-center">Secondary: </span>
              {brief.target_keywords?.secondary?.map((kw, i) => (
                <Badge key={i} variant="outline">{kw}</Badge>
              ))}
            </div>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs text-gray-500 self-center">LSI: </span>
              {brief.target_keywords?.lsi?.map((kw, i) => (
                <Badge key={i} variant="secondary">{kw}</Badge>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* FAQs */}
      <Card>
        <CardContent className="pt-6">
          <h4 className="mb-3 text-sm font-semibold">
            FAQs ({brief.faqs?.length || 0})
          </h4>
          <div className="space-y-2">
            {brief.faqs?.map((faq, i) => (
              <div key={i} className="rounded-md border p-3">
                <p className="text-sm font-medium">{faq.question}</p>
                <p className="mt-1 text-xs text-gray-600">{faq.answer}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* CTAs */}
      <Card>
        <CardContent className="pt-6">
          <h4 className="mb-3 text-sm font-semibold">CTA Placements</h4>
          <div className="space-y-2">
            {brief.ctas?.map((cta, i) => (
              <div key={i} className="flex items-center justify-between rounded-md border p-3">
                <div>
                  <Badge variant="outline" className="mr-2">{cta.position}</Badge>
                  <span className="text-sm">{cta.text}</span>
                </div>
                <span className="text-xs text-gray-400">{cta.url}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Actions */}
      <div className="flex gap-3">
        <Button variant="outline" onClick={onGenerateBrief} disabled={isGeneratingBrief}>
          Regenerate Brief
        </Button>
      </div>
    </div>
  );
}

function EditableField({
  label,
  value,
  field,
  editing,
  editValue,
  isEditable,
  onStartEdit,
  onSave,
  onCancel,
  onChange,
}: {
  label: string;
  value: string;
  field: string;
  editing: string | null;
  editValue: string;
  isEditable: boolean;
  onStartEdit: (field: string, value: string) => void;
  onSave: () => void;
  onCancel: () => void;
  onChange: (value: string) => void;
}) {
  const isEditing = editing === field;

  return (
    <div>
      <span className="text-xs font-medium text-gray-500">{label}</span>
      {isEditing ? (
        <div className="mt-1 flex gap-2">
          <Input
            value={editValue}
            onChange={(e) => onChange(e.target.value)}
            className="text-sm"
          />
          <Button size="sm" onClick={onSave}>Save</Button>
          <Button size="sm" variant="outline" onClick={onCancel}>Cancel</Button>
        </div>
      ) : (
        <div className="group flex items-center gap-2">
          <p className="text-sm">{value || <span className="text-gray-400">Not set</span>}</p>
          {isEditable && (
            <button
              onClick={() => onStartEdit(field, value)}
              className="hidden text-xs text-blue-500 hover:text-blue-700 group-hover:inline"
            >
              Edit
            </button>
          )}
        </div>
      )}
    </div>
  );
}
