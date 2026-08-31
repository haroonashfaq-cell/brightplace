export interface KeywordGap {
  id: string;
  project_id: string;
  keyword: string;
  volume: number;
  kd: number;
  intent: string | null;
  competitor_domains: string[];
  cpc: number | null;
  difficulty: string | null;
  category: string | null;
  city: string | null;
  is_long_tail: boolean | null;
  tier: string | null;
  word_count: number | null;
  fetched_at: string;
}

export interface KeywordGapList {
  items: KeywordGap[];
  total_count: number;
  page: number;
  page_size: number;
}

export interface LongTailKeyword {
  id: string;
  keyword_gap_id: string;
  keyword: string;
  volume: number;
  kd: number;
  intent: string | null;
}

export interface SelectedKeyword {
  id: string;
  project_id: string;
  keyword: string;
  volume: number;
  kd: number;
  intent: string | null;
  long_tail_keywords: LongTailKeyword[];
  status: string;
  created_at: string;
}

export interface KeywordFilters {
  kd_min?: number;
  kd_max?: number;
  vol_min?: number;
  vol_max?: number;
  intent?: string;
  search?: string;
  category?: string;
  sort_by?: string;
  sort_dir?: string;
  page?: number;
  page_size?: number;
}

// Fixed filter tabs (KD-based, always visible)
export const FIXED_TABS = [
  { label: "All", value: "" },
  { label: "Easy Wins (KD 0-10)", value: "__easy_wins" },
  { label: "Quick Wins (KD 0-15)", value: "__quick_wins" },
  { label: "Long-Tail Gold", value: "__long_tail" },
] as const;

// Hardcoded category tabs per niche
export const NICHE_CATEGORIES: Record<string, string[]> = {
  // Apartment / rental / renter niches
  apartment: [
    "Renter Education",
    "Price & Budget",
    "pet friendly",
    "Bedroom Type",
    "Property Type",
    "Near Me",
    "Student & Campus",
    "Luxury",
    "Furnished & Short-Term",
    "General",
  ],
  // Plumbing niches
  plumbing: [
    "Emergency Repairs",
    "Drain & Sewer",
    "Water Heater",
    "Fixture Installation",
    "Bathroom Plumbing",
    "Kitchen Plumbing",
    "Commercial Plumbing",
    "Pipe & Leak Repair",
    "Cost & Pricing",
    "General",
  ],
  // Real estate niches
  "real estate": [
    "Buying Guide",
    "Selling Guide",
    "Mortgage & Finance",
    "First-Time Buyer",
    "Investment Property",
    "Market Trends",
    "Home Inspection",
    "Neighborhood Guide",
    "General",
  ],
  // Default fallback
  default: ["General"],
};

export function getCategoryTabs(niche: string | null): string[] {
  if (!niche) return NICHE_CATEGORIES.default;
  const lower = niche.toLowerCase();
  for (const [key, cats] of Object.entries(NICHE_CATEGORIES)) {
    if (key === "default") continue;
    if (lower.includes(key)) return cats;
  }
  return NICHE_CATEGORIES.default;
}
