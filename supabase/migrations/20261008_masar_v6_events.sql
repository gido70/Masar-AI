-- Masar V6: anonymous usage events (decisions, feedback, uncovered requests).
-- Public visitors may INSERT only; only the Masar owner may read.
create table if not exists public.masar_v6_events (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  kind text not null check (kind in ('decision','feedback','request')),
  video_type text check (char_length(video_type) <= 40),
  tool text check (char_length(tool) <= 40),
  budget text check (char_length(budget) <= 40),
  skill text check (char_length(skill) <= 40),
  lang text check (char_length(lang) <= 40),
  useful text check (useful in ('yes','partly','no')),
  note text check (char_length(note) <= 500),
  session text check (char_length(session) <= 40)
);
alter table public.masar_v6_events enable row level security;
drop policy if exists "v6 events public insert" on public.masar_v6_events;
create policy "v6 events public insert" on public.masar_v6_events for insert to anon, authenticated with check (true);
drop policy if exists "v6 events owner read" on public.masar_v6_events;
create policy "v6 events owner read" on public.masar_v6_events for select to authenticated using (public.masar_is_owner());
revoke all on public.masar_v6_events from anon, authenticated;
grant insert (kind, video_type, tool, budget, skill, lang, useful, note, session) on public.masar_v6_events to anon, authenticated;
grant select on public.masar_v6_events to authenticated;
