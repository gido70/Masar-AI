-- Masar AI V5.5 — trainer follow-up portal
-- Safe-by-default: new accounts are pending until an owner approves them.

create extension if not exists pgcrypto;

create table if not exists public.masar_profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  role text not null default 'pending' check (role in ('pending','owner','trainer')),
  approved boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.masar_steps (
  step_no smallint primary key check (step_no between 1 and 24),
  title text not null,
  status text not null default 'waiting' check (status in ('waiting','in_progress','completed')),
  output_summary text,
  evidence_status text not null default 'not_started' check (evidence_status in ('not_started','documented','reviewed','tested')),
  updated_by uuid references public.masar_profiles(id),
  updated_at timestamptz not null default now()
);

create table if not exists public.masar_evidence (
  id uuid primary key default gen_random_uuid(),
  step_no smallint references public.masar_steps(step_no) on delete set null,
  title text not null,
  description text,
  evidence_type text not null check (evidence_type in ('document','link','video','test','version')),
  evidence_url text,
  verification_status text not null default 'documented' check (verification_status in ('documented','reviewed','tested','approved')),
  created_by uuid references public.masar_profiles(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.masar_versions (
  version text primary key,
  summary text not null,
  status text not null check (status in ('internal','review','published','archived')),
  published_url text,
  created_by uuid references public.masar_profiles(id),
  created_at timestamptz not null default now()
);

create table if not exists public.masar_trainer_feedback (
  id uuid primary key default gen_random_uuid(),
  author_id uuid not null references public.masar_profiles(id) on delete cascade,
  target_type text not null check (target_type in ('general','step','video_lab','version')),
  step_no smallint references public.masar_steps(step_no) on delete set null,
  target_label text,
  feedback_type text not null check (feedback_type in ('note','question','suggestion','approval')),
  body text not null check (char_length(body) between 2 and 4000),
  status text not null default 'new' check (status in ('new','seen','in_progress','applied','needs_discussion')),
  owner_response text,
  resolved_in_version text references public.masar_versions(version),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists masar_feedback_author_idx on public.masar_trainer_feedback(author_id, created_at desc);
create index if not exists masar_feedback_step_idx on public.masar_trainer_feedback(step_no, created_at desc);
create index if not exists masar_evidence_step_idx on public.masar_evidence(step_no, created_at desc);

create or replace function public.masar_is_owner()
returns boolean language sql stable security definer set search_path = public
as $$ select exists(select 1 from public.masar_profiles where id = auth.uid() and role = 'owner' and approved); $$;

create or replace function public.masar_can_review()
returns boolean language sql stable security definer set search_path = public
as $$ select exists(select 1 from public.masar_profiles where id = auth.uid() and role in ('owner','trainer') and approved); $$;

revoke all on function public.masar_is_owner() from public;
revoke all on function public.masar_can_review() from public;
grant execute on function public.masar_is_owner() to authenticated;
grant execute on function public.masar_can_review() to authenticated;

create or replace function public.masar_create_pending_profile()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  insert into public.masar_profiles(id, display_name, role, approved)
  values(new.id, coalesce(new.raw_user_meta_data->>'display_name', split_part(new.email,'@',1)), 'pending', false)
  on conflict (id) do nothing;
  return new;
end; $$;

drop trigger if exists masar_on_auth_user_created on auth.users;
create trigger masar_on_auth_user_created after insert on auth.users
for each row execute procedure public.masar_create_pending_profile();

alter table public.masar_profiles enable row level security;
alter table public.masar_steps enable row level security;
alter table public.masar_evidence enable row level security;
alter table public.masar_versions enable row level security;
alter table public.masar_trainer_feedback enable row level security;

revoke all on public.masar_profiles, public.masar_steps, public.masar_evidence, public.masar_versions, public.masar_trainer_feedback from anon;
grant select, insert, update, delete on public.masar_profiles, public.masar_steps, public.masar_evidence, public.masar_versions, public.masar_trainer_feedback to authenticated;

drop policy if exists "profiles read own or owner" on public.masar_profiles;
create policy "profiles read own or owner" on public.masar_profiles for select to authenticated
using (id = auth.uid() or public.masar_is_owner());
drop policy if exists "profiles owner update" on public.masar_profiles;
create policy "profiles owner update" on public.masar_profiles for update to authenticated
using (public.masar_is_owner()) with check (public.masar_is_owner());

drop policy if exists "steps approved read" on public.masar_steps;
create policy "steps approved read" on public.masar_steps for select to authenticated using (public.masar_can_review());
drop policy if exists "steps owner write" on public.masar_steps;
create policy "steps owner write" on public.masar_steps for all to authenticated using (public.masar_is_owner()) with check (public.masar_is_owner());

drop policy if exists "evidence approved read" on public.masar_evidence;
create policy "evidence approved read" on public.masar_evidence for select to authenticated using (public.masar_can_review());
drop policy if exists "evidence owner write" on public.masar_evidence;
create policy "evidence owner write" on public.masar_evidence for all to authenticated using (public.masar_is_owner()) with check (public.masar_is_owner());

drop policy if exists "versions approved read" on public.masar_versions;
create policy "versions approved read" on public.masar_versions for select to authenticated using (public.masar_can_review());
drop policy if exists "versions owner write" on public.masar_versions;
create policy "versions owner write" on public.masar_versions for all to authenticated using (public.masar_is_owner()) with check (public.masar_is_owner());

drop policy if exists "feedback read own or owner" on public.masar_trainer_feedback;
create policy "feedback read own or owner" on public.masar_trainer_feedback for select to authenticated
using (author_id = auth.uid() or public.masar_is_owner());
drop policy if exists "feedback approved insert" on public.masar_trainer_feedback;
create policy "feedback approved insert" on public.masar_trainer_feedback for insert to authenticated
with check (author_id = auth.uid() and public.masar_can_review());
drop policy if exists "feedback owner update" on public.masar_trainer_feedback;
create policy "feedback owner update" on public.masar_trainer_feedback for update to authenticated
using (public.masar_is_owner()) with check (public.masar_is_owner());

insert into public.masar_steps(step_no,title,status,output_summary,evidence_status) values
 (1,'مجال المعرفة والفكرة','completed','صياغة مجال المشكلة والمخرج','documented'),
 (2,'العميل الأساسي','completed','تحديد مستخدم عربي له مهمة وقيود','documented'),
 (3,'رحلة العميل','completed','خريطة قبل وأثناء وبعد','documented'),
 (4,'تقدير السوق الأولي','completed','فرضية سوق قابلة للتحقق','documented'),
 (5,'الاحتياجات الرئيسية','completed','الوضوح والثقة والملاءمة','documented'),
 (6,'القيمة الفريدة والمنهجية','completed','افهم، ضيق، قارن، تحقق، ابدأ، قس','documented'),
 (7,'صيغة المنتج','completed','منصة رقمية تفاعلية','documented'),
 (8,'رحلة التعلم والتحول','completed','تحول ومعايير قياس','documented'),
 (9,'مخطط المحتوى الأولي','completed','ست وحدات بنتيجة واحدة لكل وحدة','documented')
on conflict (step_no) do update set title=excluded.title,status=excluded.status,output_summary=excluded.output_summary,evidence_status=excluded.evidence_status;

insert into public.masar_steps(step_no,title,status,output_summary,evidence_status)
select i,'بانتظار شرح المدرب','waiting','لا نخمن محتوى الخطوة قبل المحاضرة','not_started'
from generate_series(10,24) i on conflict (step_no) do nothing;

insert into public.masar_versions(version,summary,status,published_url) values
 ('V5.2','خط الأساس ومختبر الفيديو الأولي','archived',null),
 ('V5.3','توسيع بطاقة المهمة والقيود وسجل القرار','internal',null),
 ('V5.4','مواءمة المنتج مع منهج المدرب والخطوات الأربع والعشرين','published','https://gido70.github.io/Masar-AI/'),
 ('V5.5','بوابة المدرب وحزمة إنتاج الفيديو','review',null)
on conflict (version) do update set summary=excluded.summary,status=excluded.status,published_url=excluded.published_url;

-- Bootstrap is intentionally manual and one-time after the owner's first login:
-- update public.masar_profiles set role='owner', approved=true where id='<OWNER_AUTH_UUID>';
-- Trainer approval after their first login:
-- update public.masar_profiles set role='trainer', approved=true where id='<TRAINER_AUTH_UUID>';
