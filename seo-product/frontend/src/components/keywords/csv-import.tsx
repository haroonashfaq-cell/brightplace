"use client";

import { useState, useRef } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import Papa from "papaparse";
import { keywordsApi } from "@/lib/api-client";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface Props {
  projectId: string;
  open: boolean;
  onClose: () => void;
}

interface ParsedKeyword {
  keyword: string;
  volume: number;
  kd: number;
  cpc: number;
  intent?: string;
  category?: string;
  city?: string;
}

// Map common CSV column name variations to our field names
function normalizeHeader(header: string): string {
  const h = header.toLowerCase().trim();
  if (h === "keyword" || h === "keywords" || h === "query" || h === "search term") return "keyword";
  if (h === "volume" || h === "search volume" || h === "vol" || h === "avg. monthly searches") return "volume";
  if (h === "kd" || h === "keyword difficulty" || h === "difficulty" || h === "kd%") return "kd";
  if (h === "cpc" || h === "cost per click" || h === "avg. cpc") return "cpc";
  if (h === "intent" || h === "search intent") return "intent";
  if (h === "category" || h === "primary category" || h === "topic") return "category";
  if (h === "city" || h === "cities" || h === "location") return "city";
  return h;
}

export function CsvImport({ projectId, open, onClose }: Props) {
  const queryClient = useQueryClient();
  const fileRef = useRef<HTMLInputElement>(null);
  const [parsed, setParsed] = useState<ParsedKeyword[]>([]);
  const [fileName, setFileName] = useState("");
  const [error, setError] = useState("");
  const [replaceExisting, setReplaceExisting] = useState(false);

  const importMutation = useMutation({
    mutationFn: () => keywordsApi.importKeywords(projectId, parsed, replaceExisting),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["keyword-gaps", projectId] });
      queryClient.invalidateQueries({ queryKey: ["keyword-categories", projectId] });
      setParsed([]);
      setFileName("");
      onClose();
    },
  });

  function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setError("");
    setFileName(file.name);

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete(results) {
        const rows = results.data as Record<string, string>[];
        if (rows.length === 0) {
          setError("CSV file is empty");
          return;
        }

        // Normalize headers
        const keywords: ParsedKeyword[] = [];
        for (const row of rows) {
          const normalized: Record<string, string> = {};
          for (const [key, value] of Object.entries(row)) {
            normalized[normalizeHeader(key)] = value;
          }

          const keyword = normalized.keyword?.trim();
          if (!keyword) continue;

          keywords.push({
            keyword,
            volume: parseInt(normalized.volume) || 0,
            kd: parseInt(normalized.kd) || 0,
            cpc: parseFloat(normalized.cpc) || 0,
            intent: normalized.intent || undefined,
            category: normalized.category || undefined,
            city: normalized.city || undefined,
          });
        }

        if (keywords.length === 0) {
          setError("No valid keywords found. Make sure your CSV has a 'Keyword' column.");
          return;
        }

        setParsed(keywords);
      },
      error(err) {
        setError(`Failed to parse CSV: ${err.message}`);
      },
    });
  }

  function handleClose() {
    setParsed([]);
    setFileName("");
    setError("");
    onClose();
  }

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>Import Keywords from CSV</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          {/* Instructions */}
          <div className="rounded-md bg-gray-50 p-3 text-sm text-gray-600">
            <p className="font-medium mb-1">Supported columns:</p>
            <p>Keyword (required), Volume, KD, CPC, Intent, Category, City</p>
            <p className="mt-1 text-xs text-gray-400">
              Works with exports from SEMrush, Ahrefs, DataForSEO, or any CSV with a Keyword column.
            </p>
          </div>

          {/* File input */}
          <div>
            <input
              ref={fileRef}
              type="file"
              accept=".csv,.tsv,.txt"
              onChange={handleFile}
              className="hidden"
            />
            <Button
              variant="outline"
              className="w-full"
              onClick={() => fileRef.current?.click()}
            >
              {fileName || "Choose CSV file"}
            </Button>
          </div>

          {error && <p className="text-sm text-red-600">{error}</p>}

          {/* Preview */}
          {parsed.length > 0 && (
            <>
              <div className="rounded-md border">
                <div className="border-b bg-gray-50 px-3 py-2 text-sm font-medium">
                  Preview ({parsed.length.toLocaleString()} keywords)
                </div>
                <div className="max-h-48 overflow-y-auto">
                  <table className="w-full text-xs">
                    <thead>
                      <tr className="border-b text-left text-gray-500">
                        <th className="px-3 py-1.5">Keyword</th>
                        <th className="px-3 py-1.5 text-right">Vol</th>
                        <th className="px-3 py-1.5 text-right">KD</th>
                        <th className="px-3 py-1.5">Category</th>
                      </tr>
                    </thead>
                    <tbody>
                      {parsed.slice(0, 10).map((kw, i) => (
                        <tr key={i} className="border-t">
                          <td className="px-3 py-1.5 truncate max-w-[180px]">
                            {kw.keyword}
                          </td>
                          <td className="px-3 py-1.5 text-right tabular-nums">
                            {kw.volume.toLocaleString()}
                          </td>
                          <td className="px-3 py-1.5 text-right tabular-nums">
                            {kw.kd}
                          </td>
                          <td className="px-3 py-1.5 text-gray-500">
                            {kw.category || "-"}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {parsed.length > 10 && (
                    <p className="border-t px-3 py-1.5 text-xs text-gray-400">
                      ...and {(parsed.length - 10).toLocaleString()} more
                    </p>
                  )}
                </div>
              </div>

              {/* Replace toggle */}
              <label className="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={replaceExisting}
                  onChange={(e) => setReplaceExisting(e.target.checked)}
                  className="rounded"
                />
                Replace all existing keywords (otherwise appends)
              </label>

              {/* Import button */}
              <Button
                className="w-full"
                onClick={() => importMutation.mutate()}
                disabled={importMutation.isPending}
              >
                {importMutation.isPending
                  ? "Importing..."
                  : `Import ${parsed.length.toLocaleString()} keywords`}
              </Button>
            </>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
