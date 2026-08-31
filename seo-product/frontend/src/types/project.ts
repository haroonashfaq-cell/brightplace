export interface Project {
  id: string;
  user_id: string;
  domain: string;
  niche: string | null;
  brand_context: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface Competitor {
  id: string;
  project_id: string;
  domain: string;
  dr_score: number | null;
  indexed_pages: number | null;
  auto_detected: boolean;
  created_at: string;
}
