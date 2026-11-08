create table if not exists public.nutrition_analyses (
    id bigint generated always as identity primary key,
    created_at timestamptz not null default now(),
    is_food boolean not null,
    items text[] not null default '{}',
    calories_kcal numeric not null check (calories_kcal >= 0),
    protein_g numeric not null check (protein_g >= 0),
    carbs_g numeric not null check (carbs_g >= 0),
    fat_g numeric not null check (fat_g >= 0),
    health_note text not null
);

alter table public.nutrition_analyses enable row level security;
