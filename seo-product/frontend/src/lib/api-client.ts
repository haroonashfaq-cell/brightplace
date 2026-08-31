import { createClient } from "@/lib/supabase/client";
import type { Project, Competitor } from "@/types/project";
import type {
  KeywordGapList,
  LongTailKeyword,
  SelectedKeyword,
  KeywordFilters,
} from "@/types/keyword";
import type {
  PipelineStatus,
  ResearchReport,
  Brief,
  BriefUpdate,
  Article,
} from "@/types/pipeline";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getToken(): Promise<string> {
  const supabase = createClient();
  const {
    data: { session },
  } = await supabase.auth.getSession();
  return session?.access_token || "";
}

async function api<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getToken();
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...options.headers,
    },
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "API error");
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

// Projects
export const projectsApi = {
  create: (data: { domain: string; niche?: string }) =>
    api<Project>("/api/projects", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  list: () => api<Project[]>("/api/projects"),

  get: (id: string) => api<Project>(`/api/projects/${id}`),

  delete: (id: string) =>
    api<void>(`/api/projects/${id}`, { method: "DELETE" }),

  detectCompetitors: (projectId: string) =>
    api<Competitor[]>(`/api/projects/${projectId}/competitors/detect`, {
      method: "POST",
    }),

  addCompetitor: (projectId: string, domain: string) =>
    api<Competitor>(`/api/projects/${projectId}/competitors`, {
      method: "POST",
      body: JSON.stringify({ domain }),
    }),

  listCompetitors: (projectId: string) =>
    api<Competitor[]>(`/api/projects/${projectId}/competitors`),

  deleteCompetitor: (projectId: string, competitorId: string) =>
    api<void>(`/api/projects/${projectId}/competitors/${competitorId}`, {
      method: "DELETE",
    }),
};

// Keywords
export const keywordsApi = {
  getGaps: (projectId: string, filters?: KeywordFilters) => {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== "") {
          params.set(key, String(value));
        }
      });
    }
    const qs = params.toString();
    return api<KeywordGapList>(
      `/api/projects/${projectId}/keyword-gaps${qs ? `?${qs}` : ""}`
    );
  },

  getCategories: (projectId: string) =>
    api<{ category: string; count: number }[]>(
      `/api/projects/${projectId}/keyword-gaps/categories`
    ),

  refreshGaps: (projectId: string) =>
    api<{ items_count: number; total_count: number }>(
      `/api/projects/${projectId}/keyword-gaps/refresh`,
      { method: "POST" }
    ),

  importKeywords: (
    projectId: string,
    keywords: Array<{
      keyword: string;
      volume?: number;
      kd?: number;
      cpc?: number;
      intent?: string;
      category?: string;
      city?: string;
    }>,
    replace: boolean = false
  ) =>
    api<{ imported: number }>(
      `/api/projects/${projectId}/keyword-gaps/import`,
      {
        method: "POST",
        body: JSON.stringify({ keywords, replace }),
      }
    ),

  getLongTail: (projectId: string, gapId: string) =>
    api<LongTailKeyword[]>(
      `/api/projects/${projectId}/keyword-gaps/${gapId}/long-tail`
    ),

  addSelected: (
    projectId: string,
    data: {
      keyword: string;
      volume: number;
      kd: number;
      intent?: string | null;
      long_tail_keywords?: Array<Record<string, unknown>>;
    }
  ) =>
    api<SelectedKeyword>(`/api/projects/${projectId}/selected-keywords`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  listSelected: (projectId: string) =>
    api<SelectedKeyword[]>(`/api/projects/${projectId}/selected-keywords`),

  deleteSelected: (projectId: string, keywordId: string) =>
    api<void>(`/api/projects/${projectId}/selected-keywords/${keywordId}`, {
      method: "DELETE",
    }),
};

// Pipeline
export const pipelineApi = {
  getStatus: (projectId: string, keywordId: string) =>
    api<PipelineStatus>(
      `/api/projects/${projectId}/keywords/${keywordId}/pipeline`
    ),

  startResearch: (projectId: string, keywordId: string) =>
    api<ResearchReport>(
      `/api/projects/${projectId}/keywords/${keywordId}/research`,
      { method: "POST" }
    ),

  getResearch: (projectId: string, keywordId: string) =>
    api<ResearchReport>(
      `/api/projects/${projectId}/keywords/${keywordId}/research`
    ),

  generateBrief: (projectId: string, keywordId: string) =>
    api<Brief>(
      `/api/projects/${projectId}/keywords/${keywordId}/brief`,
      { method: "POST" }
    ),

  getBrief: (projectId: string, briefId: string) =>
    api<Brief>(`/api/projects/${projectId}/briefs/${briefId}`),

  updateBrief: (projectId: string, briefId: string, data: BriefUpdate) =>
    api<Brief>(`/api/projects/${projectId}/briefs/${briefId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  approveBrief: (projectId: string, briefId: string) =>
    api<Brief>(`/api/projects/${projectId}/briefs/${briefId}/approve`, {
      method: "POST",
    }),

  writeArticle: (projectId: string, briefId: string) =>
    api<Article>(`/api/projects/${projectId}/briefs/${briefId}/write`, {
      method: "POST",
    }),

  getArticle: (projectId: string, articleId: string) =>
    api<Article>(`/api/projects/${projectId}/articles/${articleId}`),

  runQa: (projectId: string, articleId: string) =>
    api<Article>(`/api/projects/${projectId}/articles/${articleId}/qa`, {
      method: "POST",
    }),

  rewriteFromQa: (projectId: string, articleId: string) =>
    api<Article>(`/api/projects/${projectId}/articles/${articleId}/rewrite`, {
      method: "POST",
    }),

  exportArticle: async (projectId: string, articleId: string, format: "md" | "html" = "md") => {
    const token = await getToken();
    const res = await fetch(
      `${API_URL}/api/projects/${projectId}/articles/${articleId}/export?format=${format}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    if (!res.ok) throw new Error("Export failed");
    const blob = await res.blob();
    const filename =
      res.headers.get("Content-Disposition")?.split("filename=")[1]?.replace(/"/g, "") ||
      `article.${format}`;
    return { blob, filename };
  },

  saveSitemap: (projectId: string, sitemapUrl: string) =>
    api<{ sitemap_url: string; url_count: number }>(
      `/api/projects/${projectId}/sitemap`,
      { method: "POST", body: JSON.stringify({ sitemap_url: sitemapUrl }) }
    ),

  getSitemap: (projectId: string) =>
    api<{ urls: string[]; count: number }>(
      `/api/projects/${projectId}/sitemap`
    ),

  getGuidelines: (projectId: string) =>
    api<{ writing: Record<string, unknown>; qa: Record<string, unknown> }>(
      `/api/projects/${projectId}/guidelines`
    ),

  updateGuidelines: (projectId: string, data: { writing_guidelines?: Record<string, unknown>; qa_guidelines?: Record<string, unknown> }) =>
    api<{ writing: Record<string, unknown>; qa: Record<string, unknown> }>(
      `/api/projects/${projectId}/guidelines`,
      { method: "PUT", body: JSON.stringify(data) }
    ),
};
