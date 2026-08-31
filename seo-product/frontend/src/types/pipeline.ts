export interface SerpItem {
  position: number;
  title: string;
  url: string;
  description: string;
  domain?: string;
}

export interface ResearchReport {
  id: string;
  keyword_id: string;
  project_id: string;
  keyword: string;
  serp_data: {
    organic_results: SerpItem[];
    featured_snippet: {
      title: string;
      description: string;
      url: string;
    } | null;
    paa_questions_raw: string[];
    total_results: number;
  };
  paa_data: {
    questions: {
      question: string;
      competitor_answers: boolean;
      gap: boolean;
      priority: string;
    }[];
    additional_questions: string[];
  };
  reddit_data: {
    pain_points: string[];
    real_numbers: string[];
    misconceptions: string[];
    advice: string[];
    common_questions: string[];
    sentiment: string;
    thread_count: number;
  };
  ai_mode_data: Record<string, unknown>;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OutlineSection {
  heading: string;
  level: number;
  instructions: string;
  subsections: OutlineSection[];
}

export interface FaqItem {
  question: string;
  answer: string;
}

export interface CtaPlacement {
  position: string;
  text: string;
  url: string;
}

export interface InternalLink {
  text: string;
  url: string;
  context: string;
}

export interface Brief {
  id: string;
  research_report_id: string;
  project_id: string;
  keyword: string;
  title: string | null;
  seo_title: string | null;
  meta_description: string | null;
  slug: string | null;
  outline: OutlineSection[];
  target_keywords: {
    primary: string;
    secondary: string[];
    lsi: string[];
  };
  entities: string[];
  faqs: FaqItem[];
  ctas: CtaPlacement[];
  internal_links: InternalLink[];
  word_count_target: number;
  snippet_paragraph: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface BriefUpdate {
  title?: string;
  seo_title?: string;
  meta_description?: string;
  slug?: string;
  outline?: OutlineSection[];
  target_keywords?: Record<string, unknown>;
  entities?: string[];
  faqs?: FaqItem[];
  ctas?: CtaPlacement[];
  internal_links?: InternalLink[];
  word_count_target?: number;
  snippet_paragraph?: string;
}

export interface QaCheck {
  name: string;
  passed: boolean;
  issues: string[];
  suggestions: string[];
}

export interface QaReport {
  checks: QaCheck[];
  passed: number;
  total: number;
  score: number;
  all_passed: boolean;
}

export interface Article {
  id: string;
  brief_id: string;
  project_id: string;
  keyword: string;
  title: string | null;
  content_md: string | null;
  content_html: string | null;
  word_count: number;
  seo_score: number;
  qa_report: QaReport | Record<string, never>;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface PipelineJob {
  id: string;
  project_id: string;
  keyword_id: string;
  step: string;
  status: string;
  result: Record<string, unknown>;
  error: string | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
}

export interface PipelineStatus {
  keyword_id: string;
  keyword: string;
  steps: Record<string, PipelineJob | null>;
  research_report: ResearchReport | null;
  brief: Brief | null;
  article: Article | null;
}

export type PipelineStep = "research" | "brief" | "write" | "qa";

export const PIPELINE_STEPS: { key: PipelineStep; label: string }[] = [
  { key: "research", label: "Research" },
  { key: "brief", label: "Brief" },
  { key: "write", label: "Write" },
  { key: "qa", label: "QA" },
];
