ALTER TABLE packing_job
    ADD COLUMN trace_id VARCHAR(64) NOT NULL DEFAULT 'legacy' AFTER public_id,
    ADD KEY idx_packing_job_trace_id (trace_id);
