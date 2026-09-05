ALTER TABLE packing_job
    DROP INDEX idx_packing_job_claim,
    ADD INDEX idx_packing_job_claim (
        status ASC,
        available_at ASC,
        priority DESC,
        created_at ASC,
        id ASC
    );
