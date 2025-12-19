-- =========================
-- TABELA: product_categories
-- =========================
create table product_categories (
    id bigint auto_increment primary key,
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
    id bigint auto_increment primary key,
    name varchar(150) not null,
    description varchar(255),
    price decimal(12,2) not null,
    image_url varchar(500),
    preparation_time int not null,
    category_id bigint not null,
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
insert into product_categories (name, description) values
('Lanche', 'Sanduíches e hambúrgueres'),
('Acompanhamento', 'Batatas, saladas e outros acompanhamentos'),
('Bebida', 'Refrigerantes, sucos e outras bebidas'),
('Sobremesa', 'Doces e sobremesas');

-- =========================
-- SEED: products
-- =========================
insert into products
(name, description, price, image_url, preparation_time, category_id)
values
('Hambúrguer Clássico',
 'Pão, carne, queijo, alface e tomate',
 18.90,
 'https://images.unsplash.com/photo-1550547660-d9450f859349',
 15,
 (select id from product_categories where name = 'Lanche')
),

('Cheeseburger Bacon',
 'Hambúrguer com queijo e bacon crocante',
 22.50,
 'https://images.unsplash.com/photo-1553979459-d2229ba7433b',
 18,
 (select id from product_categories where name = 'Lanche')
),

('Batata Frita',
 'Porção de batatas fritas crocantes',
 9.90,
 'https://images.unsplash.com/photo-1598679253544-2c97992403ea',
 8,
 (select id from product_categories where name = 'Acompanhamento')
),

('Onion Rings',
 'Anéis de cebola empanados',
 11.50,
 'https://images.unsplash.com/photo-1639024471283-03518883512d',
 10,
 (select id from product_categories where name = 'Acompanhamento')
),

('Refrigerante Lata',
 '350ml - Coca-Cola, Guaraná ou Fanta',
 6.00,
 'https://images.unsplash.com/photo-1527960471264-932f39eb5846',
 2,
 (select id from product_categories where name = 'Bebida')
),

('Suco Natural',
 'Suco de laranja ou limão',
 7.50,
 'https://images.unsplash.com/photo-1600271886742-f049cd451bba',
 3,
 (select id from product_categories where name = 'Bebida')
),

('Sorvete',
 'Sorvete',
 14.00,
 'https://images.unsplash.com/photo-1497034825429-c343d7c6a68f',
 7,
 (select id from product_categories where name = 'Sobremesa')
),

('Petit Gateau',
 'Bolo de chocolate com recheio cremoso e sorvete',
 16.00,
 'https://t4.ftcdn.net/jpg/02/21/31/01/240_F_221310131_cUVS5tnUMG1qv3GWzzj8w2bgDUtLSmRv.jpg',
 10,
 (select id from product_categories where name = 'Sobremesa')
);
