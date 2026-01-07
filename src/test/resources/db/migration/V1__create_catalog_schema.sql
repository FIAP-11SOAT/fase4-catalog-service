-- =========================
-- TABELA: product_categories
-- =========================
create table product_categories (
    id uuid default random_uuid() primary key,
    name varchar(100) not null,
    description varchar(255),
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp
);

create unique index uq_product_categories_name
    on product_categories (name);

create index idx_product_categories_created_at
    on product_categories (created_at);

-- =========================
-- TABELA: products
-- =========================
create table products (
    id uuid default random_uuid() primary key,
    name varchar(150) not null,
    description varchar(255),
    price decimal(12,2) not null,
    image_url varchar(500),
    preparation_time int not null,
    category_id uuid not null,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    constraint fk_products_category
        foreign key (category_id) references product_categories(id)
);

create unique index uq_products_name
    on products (name);

create index idx_products_category_id
    on products (category_id);

create index idx_products_price
    on products (price);

create index idx_products_created_at
    on products (created_at);

-- =========================
-- SEED: product_categories
-- =========================
insert into product_categories (id, name, description) values
(UUID '11111111-1111-1111-1111-111111111111', 'Lanche',        'Sanduíches e hambúrgueres'),
(UUID '22222222-2222-2222-2222-222222222222', 'Acompanhamento','Batatas, saladas e outros acompanhamentos'),
(UUID '33333333-3333-3333-3333-333333333333', 'Bebida',        'Refrigerantes, sucos e outras bebidas'),
(UUID '44444444-4444-4444-4444-444444444444', 'Sobremesa',     'Doces e sobremesas');

-- =========================
-- SEED: products
-- =========================
insert into products
(id, name, description, price, image_url, preparation_time, category_id)
values
(UUID 'aaaaaaaa-0000-0000-0000-000000000001',
 'Hambúrguer Clássico',
 'Pão, carne, queijo, alface e tomate',
 18.90,
 'https://images.unsplash.com/photo-1550547660-d9450f859349',
 15,
 UUID '11111111-1111-1111-1111-111111111111'
),

(UUID 'aaaaaaaa-0000-0000-0000-000000000002',
 'Cheeseburger Bacon',
 'Hambúrguer com queijo e bacon crocante',
 22.50,
 'https://images.unsplash.com/photo-1553979459-d2229ba7433b',
 18,
 UUID '11111111-1111-1111-1111-111111111111'
),

(UUID 'aaaaaaaa-0000-0000-0000-000000000003',
 'Batata Frita',
 'Porção de batatas fritas crocantes',
 9.90,
 'https://images.unsplash.com/photo-1598679253544-2c97992403ea',
 8,
 UUID '22222222-2222-2222-2222-222222222222'
),

(UUID 'aaaaaaaa-0000-0000-0000-000000000004',
 'Onion Rings',
 'Anéis de cebola empanados',
 11.50,
 'https://images.unsplash.com/photo-1639024471283-03518883512d',
 10,
 UUID '22222222-2222-2222-2222-222222222222'
),

(UUID 'aaaaaaaa-0000-0000-0000-000000000005',
 'Refrigerante Lata',
 '350ml - Coca-Cola, Guaraná ou Fanta',
 6.00,
 'https://images.unsplash.com/photo-1527960471264-932f39eb5846',
 2,
 UUID '33333333-3333-3333-3333-333333333333'
),

(UUID 'aaaaaaaa-0000-0000-0000-000000000006',
 'Suco Natural',
 'Suco de laranja ou limão',
 7.50,
 'https://images.unsplash.com/photo-1600271886742-f049cd451bba',
 3,
 UUID '33333333-3333-3333-3333-333333333333'
),

(UUID 'aaaaaaaa-0000-0000-0000-000000000007',
 'Sorvete',
 'Sorvete',
 14.00,
 'https://images.unsplash.com/photo-1497034825429-c343d7c6a68f',
 7,
 UUID '44444444-4444-4444-4444-444444444444'
),

(UUID 'aaaaaaaa-0000-0000-0000-000000000008',
 'Petit Gateau',
 'Bolo de chocolate com recheio cremoso e sorvete',
 16.00,
 'https://t4.ftcdn.net/jpg/02/21/31/01/240_F_221310131_cUVS5tnUMG1qv3GWzzj8w2bgDUtLSmRv.jpg',
 10,
 UUID '44444444-4444-4444-4444-444444444444'
);
