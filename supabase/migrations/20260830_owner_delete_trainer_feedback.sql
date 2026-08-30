-- Only the approved Masar AI owner may delete trainer feedback.
drop policy if exists "feedback owner delete" on public.masar_trainer_feedback;
create policy "feedback owner delete"
on public.masar_trainer_feedback
for delete
to authenticated
using (public.masar_is_owner());
