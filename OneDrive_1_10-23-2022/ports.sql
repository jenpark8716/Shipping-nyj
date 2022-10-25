CREATE TABLE IF NOT EXISTS port(
port_id VARCHAR(10) PRIMARY KEY,
city VARCHAR(32) NOT NULL,
country VARCHAR(32) NOT NULL, 
region VARCHAR(32) NOT NULL
);

INSERT INTO port VALUES ('P1', 'Busan', 'South Korea', 'APAC');
INSERT INTO port VALUES ('P2', 'Tokyo', 'Japan', 'APAC');
INSERT INTO port VALUES ('P3', 'Mumbai', 'India', 'South Asia');
INSERT INTO port VALUES ('P4', 'Los Angeles', 'USA', 'North America');
INSERT INTO port VALUES ('P5', 'Xiamen', 'China', 'APAC');
INSERT INTO port VALUES ('P6', 'Shanghai', 'China', 'APAC');
INSERT INTO port VALUES ('P7', 'Singapore', 'Singaporea', 'APAC');
INSERT INTO port VALUES ('P8', 'Santos', 'Brazil', 'South America');
INSERT INTO port VALUES ('P9', 'Jeddah', 'Saudi Arabia', 'Gulf');
INSERT INTO port VALUES ('P10', 'Tenger Med', 'Morocco', 'Africa');
INSERT INTO port VALUES ('P11', 'Valencia', 'Spain', 'Europe');