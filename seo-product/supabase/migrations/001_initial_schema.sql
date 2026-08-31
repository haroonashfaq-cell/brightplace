-- ============================================================
-- SEO Product: Initial Schema
-- Module 1: Keyword Research & Gap Analysis
-- ============================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- PROJECTS
-- ============================================================
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    domain TEXT NOT NULL,
    niche TEXT,
    brand_context JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_projects_user_id ON projects(user_id);

-- ============================================================
-- COMPETITORS
-- ============================================================
CREATE TABLE competitors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    domain TEXT NOT NULL,
    dr_score INTEGER,
    indexed_pages INTEGER,
    auto_detected BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_competitors_project_id ON competitors(project_id);

-- ============================================================
-- KEYWORD GAPS (cached from DataForSEO, refreshed weekly)
-- ============================================================
CREATE TABLE keyword_gaps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    keyword TEXT NOT NULL,
    volume INTEGER DEFAULT 0,
    kd INTEGER DEFAULT 0,
    intent TEXT,
    competitor_domains TEXT[],
    fetched_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_keyword_gaps_project_id ON keyword_gaps(project_id);
CREATE INDEX idx_keyword_gaps_volume ON keyword_gaps(volume DESC);
CREATE INDEX idx_keyword_gaps_kd ON keyword_gaps(kd);
CREATE INDEX idx_keyword_gaps_intent ON keyword_gaps(intent);
CREATE INDEX idx_keyword_gaps_project_filters ON keyword_gaps(project_id, kd, volume, intent);

-- ============================================================
-- LONG-TAIL KEYWORDS (related to a keyword gap)
-- ============================================================
CREATE TABLE long_tail_keywords (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keyword_gap_id UUID NOT NULL REFERENCES keyword_gaps(id) ON DELETE CASCADE,
    keyword TEXT NOT NULL,
    volume INTEGER DEFAULT 0,
    kd INTEGER DEFAULT 0,
    intent TEXT,
    fetched_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_long_tail_keyword_gap_id ON long_tail_keywords(keyword_gap_id);

-- ============================================================
-- SELECTED KEYWORDS (user's queue for content production)
-- ============================================================
CREATE TABLE selected_keywords (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    keyword TEXT NOT NULL,
    volume INTEGER DEFAULT 0,
    kd INTEGER DEFAULT 0,
    intent TEXT,
    long_tail_keywords JSONB DEFAULT '[]',
    status TEXT DEFAULT 'queued',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_selected_keywords_project_id ON selected_keywords(project_id);
CREATE INDEX idx_selected_keywords_status ON selected_keywords(status);

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE competitors ENABLE ROW LEVEL SECURITY;
ALTER TABLE keyword_gaps ENABLE ROW LEVEL SECURITY;
ALTER TABLE long_tail_keywords ENABLE ROW LEVEL SECURITY;
ALTER TABLE selected_keywords ENABLE ROW LEVEL SECURITY;

-- Projects: users can only see/modify their own
CREATE POLICY projects_select ON projects
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY projects_insert ON projects
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY projects_update ON projects
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY projects_delete ON projects
    FOR DELETE USING (auth.uid() = user_id);

-- Competitors: access through project ownership
CREATE POLICY competitors_select ON competitors
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = competitors.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY competitors_insert ON competitors
    FOR INSERT WITH CHECK (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = competitors.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY competitors_delete ON competitors
    FOR DELETE USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = competitors.project_id AND projects.user_id = auth.uid())
    );

-- Keyword gaps: access through project ownership
CREATE POLICY keyword_gaps_select ON keyword_gaps
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = keyword_gaps.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY keyword_gaps_insert ON keyword_gaps
    FOR INSERT WITH CHECK (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = keyword_gaps.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY keyword_gaps_delete ON keyword_gaps
    FOR DELETE USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = keyword_gaps.project_id AND projects.user_id = auth.uid())
    );

-- Long-tail keywords: access through keyword gap → project chain
CREATE POLICY long_tail_keywords_select ON long_tail_keywords
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM keyword_gaps
            JOIN projects ON projects.id = keyword_gaps.project_id
            WHERE keyword_gaps.id = long_tail_keywords.keyword_gap_id
            AND projects.user_id = auth.uid()
        )
    );

CREATE POLICY long_tail_keywords_insert ON long_tail_keywords
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM keyword_gaps
            JOIN projects ON projects.id = keyword_gaps.project_id
            WHERE keyword_gaps.id = long_tail_keywords.keyword_gap_id
            AND projects.user_id = auth.uid()
        )
    );

CREATE POLICY long_tail_keywords_delete ON long_tail_keywords
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM keyword_gaps
            JOIN projects ON projects.id = keyword_gaps.project_id
            WHERE keyword_gaps.id = long_tail_keywords.keyword_gap_id
            AND projects.user_id = auth.uid()
        )
    );

-- Selected keywords: access through project ownership
CREATE POLICY selected_keywords_select ON selected_keywords
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = selected_keywords.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY selected_keywords_insert ON selected_keywords
    FOR INSERT WITH CHECK (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = selected_keywords.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY selected_keywords_update ON selected_keywords
    FOR UPDATE USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = selected_keywords.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY selected_keywords_delete ON selected_keywords
    FOR DELETE USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = selected_keywords.project_id AND projects.user_id = auth.uid())
    );

-- Service role bypass (for backend API using service key)
CREATE POLICY projects_service ON projects FOR ALL USING (TRUE) WITH CHECK (TRUE);
CREATE POLICY competitors_service ON competitors FOR ALL USING (TRUE) WITH CHECK (TRUE);
CREATE POLICY keyword_gaps_service ON keyword_gaps FOR ALL USING (TRUE) WITH CHECK (TRUE);
CREATE POLICY long_tail_keywords_service ON long_tail_keywords FOR ALL USING (TRUE) WITH CHECK (TRUE);
CREATE POLICY selected_keywords_service ON selected_keywords FOR ALL USING (TRUE) WITH CHECK (TRUE);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
