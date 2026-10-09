// Copy to masar-supabase-config.js only when the Supabase project is ready.
// The publishable/anon key is public by design; security depends on RLS.
// Never place service_role or any private API key in browser code.
window.MASAR_SUPABASE_CONFIG = {
  url: "https://YOUR_PROJECT.supabase.co",
  publishableKey: "YOUR_SUPABASE_PUBLISHABLE_KEY"
};
