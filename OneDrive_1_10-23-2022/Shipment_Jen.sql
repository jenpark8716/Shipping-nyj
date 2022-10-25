CREATE TABLE IF NOT EXISTS shipment(
ship_id VARCHAR(10) PRIMARY KEY,
company VARCHAR(32) NOT NULL,
region VARCHAR(10) NOT NULL
);

INSERT INTO shipment VALUES ('S1', 'Seaways', 'APAC');
INSERT INTO shipment VALUES ('S2', 'Seaways', 'APAC');
INSERT INTO shipment VALUES ('S3', 'Seaways', 'APAC');
INSERT INTO shipment VALUES ('S4', 'MSC', 'Europe');
INSERT INTO shipment VALUES ('S5', 'MSC', 'Europe');
INSERT INTO shipment VALUES ('S6', 'MSC', 'Europe');
INSERT INTO shipment VALUES ('S7', 'COSCO', 'APAC');
INSERT INTO shipment VALUES ('S8', 'COSCO', 'APAC');
INSERT INTO shipment VALUES ('S9', 'Emirates Shipping', 'Gulf');
INSERT INTO shipment VALUES ('S10', 'Emirates Shipping', 'Gulf');

