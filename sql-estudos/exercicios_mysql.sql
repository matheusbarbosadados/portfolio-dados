SELECT DATABASE();
SHOW TABLES;
DROP TABLE produtos, pedidos;
DROP VIEW produtos_acessorios;

-- NUMERO 1

CREATE TABLE produtos(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome VARCHAR(150),
    marca VARCHAR(50),
    categoria VARCHAR(50),
    preço DECIMAL(10,2),
    estoque INT

);

SELECT * FROM produtos;

-- NUMERO 2;

INSERT INTO produtos (nome, marca, categoria, preço, estoque)
VALUES
('Notebook Dell Inspiron', 'Dell', 'Notebooks', 3200.00, 15),
('Notebook Lenovo IdeaPad', 'Lenovo', 'Notebooks', 2800.00, 10),
('Notebook Acer Aspire', 'Acer', 'Notebooks', 2400.00, 8),
('Mouse Sem Fio', 'Logitech', 'Acessorios', 120.00, 50),
('Teclado Mecanico', 'Logitech', 'Acessorios', 350.00, 30),
('Headset Gamer', 'Logitech', 'Acessorios', 480.00, 20),
('Monitor 24 Polegadas', 'Samsung', 'Monitores', 900.00, 12),
('Monitor 27 Polegadas', 'Samsung', 'Monitores', 1500.00, 7),
('Smartphone Galaxy', 'Samsung', 'Celulares', 2100.00, 25),
('Smartphone Moto G', 'Motorola', 'Celulares', 1300.00, 18),
('Notebook Samsung Book', 'Samsung', 'Notebooks', 2650.50, 6),
('Monitor 22 Polegadas', 'Dell', 'Monitores', 750.90, 14),
('Webcam Full HD', 'Logitech', 'Acessorios', 249.90, 22),
('Smartphone iPhone 13', 'Apple', 'Celulares', 4500.00, 5),
('Monitor 29 Polegadas', 'LG', 'Monitores', 1850.75, 9),
('Teclado Sem Fio', 'Dell', 'Acessorios', 199.99, 35),
('Smartphone Redmi Note', 'Xiaomi', 'Celulares', 1199.00, 20),
('Notebook Asus Vivobook', 'Asus', 'Notebooks', 3100.00, 11),
('Mouse Gamer', 'Redragon', 'Acessorios', 89.90, 40);

-- NUMERO 3

INSERT INTO produtos
VALUES (NULL, "Caixa de Som Bluetooth", "JBL", "Acessorios", 299.00, 16);

-- NUMERO 4

SELECT nome, marca, preço
FROM produtos
LIMIT 5;


-- NUMERO 5
SELECT nome, marca, preço
FROM produtos
WHERE marca = "Samsung"
ORDER BY preço DESC;

-- NUMERO 6

UPDATE produtos
SET preço = 135.00
WHERE id = 4;

-- NUMERO 7

DELETE FROM produtos
WHERE id = 10;

-- NUMERO 8

ALTER TABLE produtos
ADD COLUMN garantia_meses INT;

-- NUMERO 9
SELECT * FROM produtos;

ALTER TABLE produtos
CHANGE COLUMN garantia_meses garantia INT;

-- NUMERO 10

ALTER TABLE produtos
MODIFY COLUMN nome VARCHAR(150);

-- NUMERO 11
SELECT * FROM produtos;
ALTER TABLE produtos
DROP COLUMN garantia;

-- NUMERO 12

CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    id_produto INT,
    quantidade INT,
    data_pedido DATE
);

INSERT INTO pedidos (id_produto, quantidade, data_pedido)
VALUES
(1, 2, '2026-10-01'),
(4, 5, '2026-10-01'),
(5, 3, '2026-10-02'),
(7, 1, '2026-10-02'),
(9, 2, '2026-10-03'),
(4, 2, '2026-10-04'),
(1, 1, '2026-10-04'),
(8, 2, '2026-10-05'),
(14, 1, '2026-10-05'),
(13, 4, '2026-10-06'),
(11, 2, '2026-10-07'),
(18, 1, '2026-10-07'),
(12, 3, '2026-10-08'),
(15, 2, '2026-10-09'),
(16, 6, '2026-10-09'),
(17, 2, '2026-10-10'),
(19, 10, '2026-10-11'),
(20, 3, '2026-10-12'),
(2, 1, '2026-10-13'),
(6, 2, '2026-10-14');

SELECT *
FROM pedidos;

SELECT * FROM produtos;

SELECT nome, marca
FROM produtos
WHERE marca in ("Dell", "Samsung", "Lenovo")
;


-- NUMERO 13

SELECT nome, marca, preço
FROM produtos
WHERE preço BETWEEN 500 and 2500
ORDER BY preço ASC
;

-- NUMERO 14

SELECT nome, marca, preço
FROM produtos
WHERE nome LIKE "%Notebook%"
;

-- NUMERO 15

SELECT COUNT(DISTINCT marca) as Total_Marcas
FROM produtos;

-- NUMERO 16

SELECT AVG(preço) AS Média_produtos, MIN(preço) AS preço_minimo, MAX(preço) AS preço_maximo
FROM produtos;

-- NUMERO 17

SELECT nome, preço, FORMAT(preço,0)
FROM produtos;

SELECT FORMAT(AVG(preço),2) AS preço_médio
FROM produtos;

-- NUMERO 18

SELECT categoria, COUNT(*) as Quantidade
FROM produtos
GROUP BY categoria
;

-- NUMERO 19

SELECT marca, COUNT(*)
FROM produtos
GROUP BY marca
HAVING COUNT(*) > 2;

SELECT *
FROM produtos;

-- NUMERO 20

CREATE VIEW produtos_acessorios AS
    SELECT nome, marca, preço, categoria
    FROM produtos
    WHERE categoria = "Acessorios";

SELECT nome, marca, preço
FROM produtos_acessorios;


DROP VIEW produtos_acessorios;

-- NUMERO 21


SELECT produtos.nome, pedidos.quantidade, pedidos.data_pedido
FROM produtos
INNER JOIN pedidos
ON produtos.id = pedidos.id_produto
;

-- NUMERO 22

SELECT produtos.nome,
SUM(produtos.preço * pedidos.quantidade) as Receita_Total
FROM produtos
INNER JOIN pedidos
ON produtos.id = pedidos.id_produto
GROUP BY produtos.nome;