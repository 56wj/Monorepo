-- Retire the notification delivery store; packing_job remains the source of truth.
-- Back up the old notification table and stop old control-plane replicas before upgrade.
DROP TABLE IF EXISTS packing_outbox_event;
