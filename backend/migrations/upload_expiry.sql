-- Deployment gate: enable pg_cron in the managed DB and verify executions before accepting uploads.
-- Conservative upload-based expiry also covers failures and never-opened sessions.
SELECT cron.schedule('simmer-upload-expiry', '0 * * * *',
  $$DELETE FROM documents WHERE kind = 'upload' AND (body->>'expires_at')::timestamptz <= now()$$);
-- Expiry is upload+6d23h so hourly cleanup stays within seven days. Verify cron operation before release.
