-- Flyway Migration: V1 - Create base tables
-- idempotent DDL (IF NOT EXISTS) para re-execuções seguras

-- Tabela de categorias de produto
create table if not exists product_categories (
    id bigserial primary key,
    name varchar(100) not null unique,
    description text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists idx_product_categories_created_at on product_categories (created_at);

-- Tabela de produtos
create table if not exists products (
    id bigserial primary key,
    name varchar(150) not null unique,
    description text,
    price numeric(12,2) not null check (price >= 0),
    image_url varchar(500),
    preparation_time integer not null check (preparation_time >= 0),
    category_id bigint not null references product_categories (id) on delete restrict,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists idx_products_category_id on products (category_id);
create index if not exists idx_products_price on products (price);
create index if not exists idx_products_created_at on products (created_at);

-- Função para atualizar automaticamente o campo updated_at
create or replace function set_updated_at_column()
returns trigger as $func$
begin
    new.updated_at = now();
    return new;
end;
$func$ language plpgsql;

-- Triggers para atualizar updated_at nas tabelas
drop trigger if exists trg_set_updated_at_categories on product_categories;
create trigger trg_set_updated_at_categories
before update on product_categories
for each row
execute function set_updated_at_column();

drop trigger if exists trg_set_updated_at_products on products;
create trigger trg_set_updated_at_products
before update on products
for each row
execute function set_updated_at_column();
