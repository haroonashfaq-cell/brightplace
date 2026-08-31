"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import type { KeywordFilters } from "@/types/keyword";

interface Props {
  filters: KeywordFilters;
  onUpdate: (filters: Partial<KeywordFilters>) => void;
}

export function KeywordFilterBar({ filters, onUpdate }: Props) {
  const [search, setSearch] = useState(filters.search ?? "");

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    onUpdate({ search: search || undefined });
  }

  return (
    <div className="flex flex-wrap items-end gap-3">
      {/* Intent filter */}
      <div>
        <label className="mb-1 block text-xs font-medium text-gray-500">
          Intent
        </label>
        <select
          className="rounded-md border bg-white px-3 py-2 text-sm"
          value={filters.intent ?? ""}
          onChange={(e) =>
            onUpdate({ intent: e.target.value || undefined })
          }
        >
          <option value="">All intents</option>
          <option value="informational">Informational</option>
          <option value="commercial">Commercial</option>
          <option value="transactional">Transactional</option>
          <option value="navigational">Navigational</option>
        </select>
      </div>

      {/* KD range */}
      <div>
        <label className="mb-1 block text-xs font-medium text-gray-500">
          KD max
        </label>
        <Input
          type="number"
          className="w-20"
          placeholder="30"
          value={filters.kd_max ?? ""}
          onChange={(e) =>
            onUpdate({
              kd_max: e.target.value ? Number(e.target.value) : undefined,
            })
          }
        />
      </div>

      {/* Volume min */}
      <div>
        <label className="mb-1 block text-xs font-medium text-gray-500">
          Vol min
        </label>
        <Input
          type="number"
          className="w-24"
          placeholder="500"
          value={filters.vol_min ?? ""}
          onChange={(e) =>
            onUpdate({
              vol_min: e.target.value ? Number(e.target.value) : undefined,
            })
          }
        />
      </div>

      {/* Search */}
      <form onSubmit={handleSearch} className="flex gap-2">
        <div>
          <label className="mb-1 block text-xs font-medium text-gray-500">
            Search
          </label>
          <Input
            className="w-48"
            placeholder="Filter keywords..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <Button type="submit" variant="outline" className="self-end">
          Filter
        </Button>
      </form>
    </div>
  );
}
