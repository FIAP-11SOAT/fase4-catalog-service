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

-- Dados iniciais para product_categories
insert into product_categories (name, description) values
('Lanche', 'Sanduíches e hambúrgueres'),
('Acompanhamento', 'Batatas, saladas e outros acompanhamentos'),
('Bebida', 'Refrigerantes, sucos e outras bebidas'),
('Sobremesa', 'Doces e sobremesas')
on conflict (name) do nothing;

-- Dados iniciais para products
insert into products (name, description, price, image_url, preparation_time, category_id) values
('Hambúrguer Clássico', 'Pão, carne, queijo, alface e tomate', 18.90, 'https://images.unsplash.com/photo-1550547660-d9450f859349', 15, 1),
('Cheeseburger Bacon', 'Hambúrguer com queijo e bacon crocante', 22.50, 'https://images.unsplash.com/photo-1553979459-d2229ba7433b', 18, 1),
('Batata Frita', 'Porção de batatas fritas crocantes', 9.90, 'https://images.unsplash.com/photo-1598679253544-2c97992403ea', 8, 2),
('Onion Rings', 'Anéis de cebola empanados', 11.50, 'https://images.unsplash.com/photo-1639024471283-03518883512d', 10, 2),
('Refrigerante Lata', '350ml - Coca-Cola, Guaraná ou Fanta', 6.00, 'https://images.unsplash.com/photo-1527960471264-932f39eb5846', 2, 3),
('Suco Natural', 'Suco de laranja ou limão', 7.50, 'https://images.unsplash.com/photo-1600271886742-f049cd451bba', 3, 3),
('Sorvete', 'sorvete', 14.00, 'https://images.unsplash.com/photo-1497034825429-c343d7c6a68f', 7, 4),
('Petit Gateau', 'Bolo de chocolate com recheio cremoso e sorvete', 16.00, 'https://t4.ftcdn.net/jpg/02/21/31/01/240_F_221310131_cUVS5tnUMG1qv3GWzzj8w2bgDUtLSmRv.jpg', 10, 4)
on conflict (name) do nothing;