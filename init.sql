CREATE TABLE emails(
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL
);

CREATE TABLE systems(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    image_url TEXT NOT NULL
);

CREATE TABLE system_specs(
    id SERIAL PRIMARY KEY,
    system_id INT REFERENCES systems(id) ON DELETE CASCADE,
    spec_key VARCHAR(50) NOT NULL,
    spec_value TEXT NOT NULL
);

INSERT INTO systems (name, image_url) VALUES
('Tron-1', '/static/images/tron1.png'),
('Tron-2', '/static/images/tron2.png');

-- Specs for Tron-1 (system_id = 1)
INSERT INTO system_specs (system_id, spec_key, spec_value) VALUES
(1, 'CPU', 'Ryzen 5 PRO 220'),
(1, 'RAM', '32GB DDR4'),
(1, 'Storage', '1TB NVME SSD'),
(1, 'Display', '15.6" Touch');

-- Specs for Tron-2 (system_id = 2)
INSERT INTO system_specs (system_id, spec_key, spec_value) VALUES
(2, 'CPU', 'Intel i7-1165G7'),
(2, 'RAM', '16GB DDR4'),
(2, 'Storage', '512GB NVME SSD');