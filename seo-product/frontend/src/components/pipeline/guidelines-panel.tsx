"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { pipelineApi } from "@/lib/api-client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Props {
  projectId: string;
}

export function GuidelinesPanel({ projectId }: Props) {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<"writing" | "qa">("writing");
  const [editingField, setEditingField] = useState<string | null>(null);
  const [editValue, setEditValue] = useState("");

  const { data, isLoading } = useQuery({
    queryKey: ["guidelines", projectId],
    queryFn: () => pipelineApi.getGuidelines(projectId),
    enabled: !!projectId,
  });

  const updateMutation = useMutation({
    mutationFn: (updates: { writing_guidelines?: Record<string, unknown>; qa_guidelines?: Record<string, unknown> }) =>
      pipelineApi.updateGuidelines(projectId, updates),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["guidelines", projectId] });
      setEditingField(null);
    },
  });

  if (isLoading || !data) {
    return <div className="text-sm text-gray-400">Loading guidelines...</div>;
  }

  const writing = data.writing as Record<string, unknown>;
  const qa = data.qa as Record<string, unknown>;

  const updateWritingField = (key: string, value: unknown) => {
    const updated = { ...writing, [key]: value };
    updateMutation.mutate({ writing_guidelines: updated });
  };

  const updateBannedPhrases = (phrases: string[]) => {
    updateWritingField("banned_phrases", phrases);
  };

  const removeBannedPhrase = (phrase: string) => {
    const current = (writing.banned_phrases as string[]) || [];
    updateBannedPhrases(current.filter((p) => p !== phrase));
  };

  const addBannedPhrase = () => {
    if (!editValue.trim()) return;
    const current = (writing.banned_phrases as string[]) || [];
    if (!current.includes(editValue.trim().toLowerCase())) {
      updateBannedPhrases([...current, editValue.trim().toLowerCase()]);
    }
    setEditValue("");
    setEditingField(null);
  };

  return (
    <div className="space-y-4">
      {/* Tabs */}
      <div className="flex gap-1 rounded-lg border bg-white p-1">
        <button
          onClick={() => setActiveTab("writing")}
          className={`rounded-md px-4 py-1.5 text-sm font-medium transition-colors ${
            activeTab === "writing" ? "bg-gray-900 text-white" : "text-gray-600 hover:bg-gray-100"
          }`}
        >
          Writing Guidelines
        </button>
        <button
          onClick={() => setActiveTab("qa")}
          className={`rounded-md px-4 py-1.5 text-sm font-medium transition-colors ${
            activeTab === "qa" ? "bg-gray-900 text-white" : "text-gray-600 hover:bg-gray-100"
          }`}
        >
          QA Guidelines
        </button>
      </div>

      {activeTab === "writing" && (
        <div className="space-y-3">
          {/* Structure */}
          <Card>
            <CardContent className="pt-6">
              <h4 className="mb-3 text-sm font-semibold">Content Structure</h4>
              <div className="grid gap-3 sm:grid-cols-2">
                <FieldRow label="Max Word Count" value={String(writing.max_word_count || 2500)} onSave={(v) => updateWritingField("max_word_count", parseInt(v))} />
                <FieldRow label="FAQ Count" value={String(writing.faq_count || "6-8")} onSave={(v) => updateWritingField("faq_count", v)} />
                <FieldRow label="CTA Count" value={String(writing.cta_count || 3)} onSave={(v) => updateWritingField("cta_count", parseInt(v))} />
                <FieldRow label="Internal Links" value={String(writing.internal_links || "5-10")} onSave={(v) => updateWritingField("internal_links", v)} />
                <FieldRow label="External Links" value={String(writing.external_links || "3-5")} onSave={(v) => updateWritingField("external_links", v)} />
                <FieldRow label="Section Length" value={String(writing.section_length || "120-180 words")} onSave={(v) => updateWritingField("section_length", v)} />
                <FieldRow label="Snippet Length" value={String(writing.snippet_length || "49-55 words")} onSave={(v) => updateWritingField("snippet_length", v)} />
                <FieldRow label="URL Path" value={String(writing.url_path || "/resources/")} onSave={(v) => updateWritingField("url_path", v)} />
              </div>
            </CardContent>
          </Card>

          {/* CTAs */}
          <Card>
            <CardContent className="pt-6">
              <h4 className="mb-3 text-sm font-semibold">CTA Domains</h4>
              <div className="grid gap-3 sm:grid-cols-2">
                <FieldRow label="Brand URL" value={String((writing.cta_domains as Record<string, string>)?.brand || "")} onSave={(v) => updateWritingField("cta_domains", { ...(writing.cta_domains as Record<string, string>), brand: v })} />
                <FieldRow label="Action URL" value={String((writing.cta_domains as Record<string, string>)?.action || "")} onSave={(v) => updateWritingField("cta_domains", { ...(writing.cta_domains as Record<string, string>), action: v })} />
              </div>
            </CardContent>
          </Card>

          {/* Banned Phrases */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-3">
                <h4 className="text-sm font-semibold">Banned Phrases</h4>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setEditingField("add_phrase")}
                  className="h-7 text-xs"
                >
                  + Add
                </Button>
              </div>
              {editingField === "add_phrase" && (
                <div className="mb-3 flex gap-2">
                  <Input
                    value={editValue}
                    onChange={(e) => setEditValue(e.target.value)}
                    placeholder="New banned phrase"
                    className="text-sm"
                    onKeyDown={(e) => e.key === "Enter" && addBannedPhrase()}
                  />
                  <Button size="sm" onClick={addBannedPhrase}>Add</Button>
                  <Button size="sm" variant="outline" onClick={() => { setEditingField(null); setEditValue(""); }}>Cancel</Button>
                </div>
              )}
              <div className="flex flex-wrap gap-1.5">
                {((writing.banned_phrases as string[]) || []).map((phrase) => (
                  <Badge key={phrase} variant="secondary" className="gap-1 pr-1">
                    {phrase}
                    <button
                      onClick={() => removeBannedPhrase(phrase)}
                      className="ml-0.5 rounded-full p-0.5 hover:bg-gray-300"
                    >
                      <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Banned Sources */}
          <Card>
            <CardContent className="pt-6">
              <h4 className="mb-3 text-sm font-semibold">Banned Sources (never link to)</h4>
              <div className="flex flex-wrap gap-1.5">
                {((writing.banned_sources as string[]) || []).map((src) => (
                  <Badge key={src} variant="outline" className="text-xs">
                    {src}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Toggles */}
          <Card>
            <CardContent className="pt-6">
              <h4 className="mb-3 text-sm font-semibold">Rules</h4>
              <div className="space-y-2">
                <ToggleRow label="Brand name always lowercase" checked={!!writing.brand_name_lowercase} onChange={(v) => updateWritingField("brand_name_lowercase", v)} />
                <ToggleRow label="No em dashes" checked={!!writing.no_em_dashes} onChange={(v) => updateWritingField("no_em_dashes", v)} />
                <ToggleRow label="Fair Housing compliance" checked={!!writing.fair_housing} onChange={(v) => updateWritingField("fair_housing", v)} />
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {activeTab === "qa" && (
        <div className="space-y-3">
          <Card>
            <CardContent className="pt-6">
              <h4 className="mb-3 text-sm font-semibold">QA Checks</h4>
              <div className="space-y-2">
                {((qa.checks as Array<{ name: string; enabled: boolean; description: string }>) || []).map((check, i) => (
                  <div key={check.name} className="flex items-center justify-between rounded-md border p-3">
                    <div>
                      <p className="text-sm font-medium">{check.name}</p>
                      <p className="text-xs text-gray-500">{check.description}</p>
                    </div>
                    <label className="relative inline-flex cursor-pointer items-center">
                      <input
                        type="checkbox"
                        checked={check.enabled}
                        onChange={(e) => {
                          const checks = [...((qa.checks as Array<{ name: string; enabled: boolean; description: string }>) || [])];
                          checks[i] = { ...checks[i], enabled: e.target.checked };
                          updateMutation.mutate({ qa_guidelines: { ...qa, checks } });
                        }}
                        className="peer sr-only"
                      />
                      <div className="h-5 w-9 rounded-full bg-gray-200 after:absolute after:left-[2px] after:top-[2px] after:h-4 after:w-4 after:rounded-full after:bg-white after:transition-all peer-checked:bg-gray-900 peer-checked:after:translate-x-full" />
                    </label>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <h4 className="mb-3 text-sm font-semibold">Known Broken URLs (never link to)</h4>
              <div className="space-y-1">
                {((qa.broken_urls as string[]) || []).map((url) => (
                  <p key={url} className="text-xs text-gray-600 font-mono">{url}</p>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}

function FieldRow({ label, value, onSave }: { label: string; value: string; onSave: (v: string) => void }) {
  const [editing, setEditing] = useState(false);
  const [v, setV] = useState(value);

  if (editing) {
    return (
      <div>
        <span className="text-xs text-gray-500">{label}</span>
        <div className="flex gap-1 mt-0.5">
          <Input value={v} onChange={(e) => setV(e.target.value)} className="h-8 text-sm" />
          <Button size="sm" className="h-8" onClick={() => { onSave(v); setEditing(false); }}>OK</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="group cursor-pointer" onClick={() => setEditing(true)}>
      <span className="text-xs text-gray-500">{label}</span>
      <p className="text-sm font-medium group-hover:text-blue-600">{value}</p>
    </div>
  );
}

function ToggleRow({ label, checked, onChange }: { label: string; checked: boolean; onChange: (v: boolean) => void }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-sm">{label}</span>
      <label className="relative inline-flex cursor-pointer items-center">
        <input type="checkbox" checked={checked} onChange={(e) => onChange(e.target.checked)} className="peer sr-only" />
        <div className="h-5 w-9 rounded-full bg-gray-200 after:absolute after:left-[2px] after:top-[2px] after:h-4 after:w-4 after:rounded-full after:bg-white after:transition-all peer-checked:bg-gray-900 peer-checked:after:translate-x-full" />
      </label>
    </div>
  );
}
