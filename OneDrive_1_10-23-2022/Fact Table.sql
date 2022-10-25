CREATE TABLE shipping (
ship_id VARCHAR(10) NOT NULL,
product_id VARCHAR(10) NOT NULL,
order_quantity INT NOT NULL,
"date" date NOT NULL,
from_port VARCHAR(10) NOT NULL,
to_port VARCHAR(10) NOT NULL,
CHECK (from_port <> to_port),
FOREIGN KEY (ship_id) REFERENCES shipment (ship_id),
FOREIGN KEY (product_id) REFERENCES product_ship (product_id),
FOREIGN KEY ("date") REFERENCES date ("date"),
FOREIGN KEY (from_port) REFERENCES port (port_id),
FOREIGN KEY (to_port) REFERENCES port (port_id),
PRIMARY KEY (ship_id, "date", from_port, to_port)
);

INSERT INTO shipping
SELECT s.ship_id, ps.product_id, ceil(random()*100000000), d.date, p1.port_id, p2.port_id
FROM shipment s, product_ship ps, date d, port p1 INNER JOIN port p2 
ON p1.port_id <> p2.port_id
ORDER BY random()
limit 100;