-- Masar AI — safe capacity snapshot for approved reviewers.
-- Limits reflect the Supabase Free plan baseline on 2026-08-29.

create or replace function public.masar_capacity_snapshot()
returns jsonb
language plpgsql
stable
security definer
set search_path = public, pg_catalog
as $$
declare
  db_bytes bigint;
  storage_bytes bigint;
  auth_users bigint;
  masar_rows bigint;
  db_limit constant bigint := 500 * 1024 * 1024;
  storage_limit constant bigint := 1024 * 1024 * 1024;
begin
  if not public.masar_can_review() then
    raise exception 'not_authorized' using errcode = '42501';
  end if;
  select pg_database_size(current_database()) into db_bytes;
  select coalesce(sum(case when metadata->>'size' ~ '^[0-9]+$' then (metadata->>'size')::bigint else 0 end), 0)
    into storage_bytes from storage.objects;
  select count(*) into auth_users from auth.users;
  select (select count(*) from public.masar_profiles)
       + (select count(*) from public.masar_steps)
       + (select count(*) from public.masar_evidence)
       + (select count(*) from public.masar_versions)
       + (select count(*) from public.masar_trainer_feedback)
    into masar_rows;
  return jsonb_build_object(
    'database_bytes', db_bytes,
    'database_limit_bytes', db_limit,
    'database_ratio', round(db_bytes::numeric / db_limit, 4),
    'storage_bytes', storage_bytes,
    'storage_limit_bytes', storage_limit,
    'storage_ratio', round(storage_bytes::numeric / storage_limit, 4),
    'auth_users', auth_users,
    'masar_rows', masar_rows,
    'captured_at', now()
  );
end;
$$;

revoke all on function public.masar_capacity_snapshot() from public, anon;
grant execute on function public.masar_capacity_snapshot() to authenticated;
