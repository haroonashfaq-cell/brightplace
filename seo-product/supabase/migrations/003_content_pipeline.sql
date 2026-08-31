-- ============================================================
-- SEO Product: Content Pipeline
-- Module 2: Research → Brief → Write → QA
-- ============================================================

-- ============================================================
-- RESEARCH REPORTS
-- ============================================================
CREATE TABLE research_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keyword_id UUID NOT NULL REFERENCES selected_keywords(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    keyword TEXT NOT NULL,
    serp_data JSONB DEFAULT '{}',
    paa_data JSONB DEFAULT '{}',
    reddit_data JSONB DEFAULT '{}',
    ai_mode_data JSONB DEFAULT '{}',
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_research_reports_project_id ON research_reports(project_id);
CREATE INDEX idx_research_reports_keyword_id ON research_reports(keyword_id);
CREATE INDEX idx_research_reports_status ON research_reports(status);

-- ============================================================
-- BRIEFS (content briefs generated from research)
-- ============================================================
CREATE TABLE briefs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    research_report_id UUID NOT NULL REFERENCES research_reports(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    keyword TEXT NOT NULL,
    title TEXT,
    seo_title TEXT,
    meta_description TEXT,
    slug TEXT,
    outline JSONB DEFAULT '[]',
    target_keywords JSONB DEFAULT '{}',
    entities JSONB DEFAULT '[]',
    faqs JSONB DEFAULT '[]',
    ctas JSONB DEFAULT '[]',
    internal_links JSONB DEFAULT '[]',
    word_count_target INTEGER DEFAULT 2000,
    snippet_paragraph TEXT,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_briefs_project_id ON briefs(project_id);
CREATE INDEX idx_briefs_research_report_id ON briefs(research_report_id);
CREATE INDEX idx_briefs_status ON briefs(status);

-- ============================================================
-- ARTICLES (written content from approved briefs)
-- ============================================================
CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brief_id UUID NOT NULL REFERENCES briefs(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    keyword TEXT NOT NULL,
    title TEXT,
    content_md TEXT,
    content_html TEXT,
    word_count INTEGER DEFAULT 0,
    seo_score INTEGER DEFAULT 0,
    qa_report JSONB DEFAULT '{}',
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_articles_project_id ON articles(project_id);
CREATE INDEX idx_articles_brief_id ON articles(brief_id);
CREATE INDEX idx_articles_status ON articles(status);

-- ============================================================
-- PIPELINE JOBS (track each step of the pipeline)
-- ============================================================
CREATE TABLE pipeline_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    keyword_id UUID NOT NULL REFERENCES selected_keywords(id) ON DELETE CASCADE,
    step TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    result JSONB DEFAULT '{}',
    error TEXT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_pipeline_jobs_project_id ON pipeline_jobs(project_id);
CREATE INDEX idx_pipeline_jobs_keyword_id ON pipeline_jobs(keyword_id);
CREATE INDEX idx_pipeline_jobs_status ON pipeline_jobs(status);

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE research_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE briefs ENABLE ROW LEVEL SECURITY;
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE pipeline_jobs ENABLE ROW LEVEL SECURITY;

-- Research reports: access through project ownership
CREATE POLICY research_reports_select ON research_reports
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = research_reports.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY research_reports_insert ON research_reports
    FOR INSERT WITH CHECK (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = research_reports.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY research_reports_update ON research_reports
    FOR UPDATE USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = research_reports.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY research_reports_delete ON research_reports
    FOR DELETE USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = research_reports.project_id AND projects.user_id = auth.uid())
    );

-- Briefs: access through project ownership
CREATE POLICY briefs_select ON briefs
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = briefs.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY briefs_insert ON briefs
    FOR INSERT WITH CHECK (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = briefs.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY briefs_update ON briefs
    FOR UPDATE USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = briefs.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY briefs_delete ON briefs
    FOR DELETE USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = briefs.project_id AND projects.user_id = auth.uid())
    );

-- Articles: access through project ownership
CREATE POLICY articles_select ON articles
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = articles.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY articles_insert ON articles
    FOR INSERT WITH CHECK (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = articles.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY articles_update ON articles
    FOR UPDATE USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = articles.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY articles_delete ON articles
    FOR DELETE USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = articles.project_id AND projects.user_id = auth.uid())
    );

-- Pipeline jobs: access through project ownership
CREATE POLICY pipeline_jobs_select ON pipeline_jobs
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = pipeline_jobs.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY pipeline_jobs_insert ON pipeline_jobs
    FOR INSERT WITH CHECK (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = pipeline_jobs.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY pipeline_jobs_update ON pipeline_jobs
    FOR UPDATE USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = pipeline_jobs.project_id AND projects.user_id = auth.uid())
    );

CREATE POLICY pipeline_jobs_delete ON pipeline_jobs
    FOR DELETE USING (
        EXISTS (SELECT 1 FROM projects WHERE projects.id = pipeline_jobs.project_id AND projects.user_id = auth.uid())
    );

-- Service role bypass (for backend API using service key)
CREATE POLICY research_reports_service ON research_reports FOR ALL USING (TRUE) WITH CHECK (TRUE);
CREATE POLICY briefs_service ON briefs FOR ALL USING (TRUE) WITH CHECK (TRUE);
CREATE POLICY articles_service ON articles FOR ALL USING (TRUE) WITH CHECK (TRUE);
CREATE POLICY pipeline_jobs_service ON pipeline_jobs FOR ALL USING (TRUE) WITH CHECK (TRUE);

-- Updated_at triggers
CREATE TRIGGER research_reports_updated_at
    BEFORE UPDATE ON research_reports
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER briefs_updated_at
    BEFORE UPDATE ON briefs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER articles_updated_at
    BEFORE UPDATE ON articles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
