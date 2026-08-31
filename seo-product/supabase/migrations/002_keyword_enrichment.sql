ALTER TABLE keyword_gaps ADD COLUMN cpc NUMERIC DEFAULT 0;
ALTER TABLE keyword_gaps ADD COLUMN difficulty TEXT;
ALTER TABLE keyword_gaps ADD COLUMN category TEXT;
ALTER TABLE keyword_gaps ADD COLUMN city TEXT;
ALTER TABLE keyword_gaps ADD COLUMN is_long_tail BOOLEAN DEFAULT FALSE;
ALTER TABLE keyword_gaps ADD COLUMN tier TEXT;
ALTER TABLE keyword_gaps ADD COLUMN word_count INTEGER DEFAULT 0;
CREATE INDEX idx_keyword_gaps_category ON keyword_gaps(category);
