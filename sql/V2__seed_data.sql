-- Flyway Migration: V2 - Seed initial data (idempotent)

-- Dados iniciais para product_categories
insert into product_categories (name, description) values
('Lanche', 'Sanduíches e hambúrgueres')
on conflict (name) do nothing;

insert into product_categories (name, description) values
('Acompanhamento', 'Batatas, saladas e outros acompanhamentos')
on conflict (name) do nothing;

insert into product_categories (name, description) values
('Bebida', 'Refrigerantes, sucos e outras bebidas')
on conflict (name) do nothing;

insert into product_categories (name, description) values
('Sobremesa', 'Doces e sobremesas')
on conflict (name) do nothing;

-- Dados iniciais para products (usando subselects para garantir FK)
insert into products (name, description, price, image_url, preparation_time, category_id)
select 'Hambúrguer Clássico', 'Pão, carne, queijo, alface e tomate', 18.90,
       'https://images.unsplash.com/photo-1550547660-d9450f859349', 15,
       (select id from product_categories where name = 'Lanche')
where not exists (select 1 from products where name = 'Hambúrguer Clássico');

insert into products (name, description, price, image_url, preparation_time, category_id)
select 'Cheeseburger Bacon', 'Hambúrguer com queijo e bacon crocante', 22.50,
       'https://images.unsplash.com/photo-1553979459-d2229ba7433b', 18,
       (select id from product_categories where name = 'Lanche')
where not exists (select 1 from products where name = 'Cheeseburger Bacon');

insert into products (name, description, price, image_url, preparation_time, category_id)
select 'Batata Frita', 'Porção de batatas fritas crocantes', 9.90,
       'https://images.unsplash.com/photo-1598679253544-2c97992403ea', 8,
       (select id from product_categories where name = 'Acompanhamento')
where not exists (select 1 from products where name = 'Batata Frita');

insert into products (name, description, price, image_url, preparation_time, category_id)
select 'Onion Rings', 'Anéis de cebola empanados', 11.50,
       'https://images.unsplash.com/photo-1639024471283-03518883512d', 10,
       (select id from product_categories where name = 'Acompanhamento')
where not exists (select 1 from products where name = 'Onion Rings');

insert into products (name, description, price, image_url, preparation_time, category_id)
select 'Refrigerante Lata', '350ml - Coca-Cola, Guaraná ou Fanta', 6.00,
       'https://images.unsplash.com/photo-1527960471264-932f39eb5846', 2,
       (select id from product_categories where name = 'Bebida')
where not exists (select 1 from products where name = 'Refrigerante Lata');

insert into products (name, description, price, image_url, preparation_time, category_id)
select 'Suco Natural', 'Suco de laranja ou limão', 7.50,
       'https://images.unsplash.com/photo-1600271886742-f049cd451bba', 3,
       (select id from product_categories where name = 'Bebida')
where not exists (select 1 from products where name = 'Suco Natural');

insert into products (name, description, price, image_url, preparation_time, category_id)
select 'Sorvete', 'sorvete', 14.00,
       'https://images.unsplash.com/photo-1497034825429-c343d7c6a68f', 7,
       (select id from product_categories where name = 'Sobremesa')
where not exists (select 1 from products where name = 'Sorvete');

insert into products (name, description, price, image_url, preparation_time, category_id)
select 'Petit Gateau', 'Bolo de chocolate com recheio cremoso e sorvete', 16.00,
       'https://t4.ftcdn.net/jpg/02/21/31/01/240_F_221310131_cUVS5tnUMG1qv3GWzzj8w2bgDUtLSmRv.jpg', 10,
       (select id from product_categories where name = 'Sobremesa')
where not exists (select 1 from products where name = 'Petit Gateau');
