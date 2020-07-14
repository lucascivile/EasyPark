
CREATE TABLE usuario (
	cpf 			 CHAR(11) PRIMARY KEY,
	nome			 VARCHAR(70) NOT NULL,
	email			 VARCHAR(50) NOT NULL UNIQUE,
	senha   		 VARCHAR(50) NOT NULL,
	data_nascimento  DATE NOT NULL,
  	CONSTRAINT data_nascimento_valida CHECK(data_nascimento BETWEEN '1900-01-01' AND (NOW() - interval '18' year)),
	CONSTRAINT cpf_valido CHECK(cpf SIMILAR TO '\d{11}'),
	CONSTRAINT email_valido CHECK(email LIKE '_%@_%._%')
);

CREATE TABLE agente_municipal (
	cpf_usuario  CHAR(11) PRIMARY KEY,
	registro_municipal VARCHAR(30) UNIQUE,
	FOREIGN KEY (cpf_usuario)
		REFERENCES usuario(cpf)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE proprietario (
	cpf_usuario  		  CHAR(11) PRIMARY KEY,
	endereco_logradouro   VARCHAR(50) NOT NULL,
	endereco_numero  	  VARCHAR(5) NOT NULL,
	endereco_complemento  VARCHAR(20),
	endereco_cep 		  CHAR(8) NOT NULL,
	CONSTRAINT endereco_numero_valido CHECK(endereco_numero SIMILAR TO '\d{1,5}'),
	CONSTRAINT cep_valido CHECK(endereco_cep SIMILAR TO '\d{8}'),
	FOREIGN KEY (cpf_usuario)
		REFERENCES usuario(cpf)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	UNIQUE (endereco_cep, endereco_numero, endereco_complemento)
);

CREATE TABLE motorista (
	cpf_usuario  CHAR(11) PRIMARY KEY,
	cnh	 CHAR(11) NOT NULL UNIQUE,
	CONSTRAINT cnh_valida CHECK(cnh SIMILAR TO '\d{11}'),
	FOREIGN KEY (cpf_usuario)
		REFERENCES usuario(cpf)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE veiculo (
  	placa CHAR(7) PRIMARY KEY,
	cpf_motorista CHAR(11) NOT NULL,
	modelo VARCHAR(30) NOT NULL,
	ano INT NOT NULL,
	cor VARCHAR(15) NOT NULL,
	CONSTRAINT ano_valido CHECK(ano > 1900 AND ano < extract(year FROM CURRENT_DATE)::int + 2),
	FOREIGN KEY (cpf_motorista)
		REFERENCES motorista(cpf_usuario)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE vaga (
	id_vaga SERIAL PRIMARY KEY, 
	cpf_proprietario CHAR(11) NOT NULL,
    preco_hora DECIMAL(5, 2) NOT NULL,
	latitude REAL,
	longitude REAL,
	largura DECIMAL(4, 2),
	comprimento DECIMAL(4, 2),
	liberada BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT preco_hora_valido CHECK (preco_hora > 0),
	CONSTRAINT largura_valida CHECK (largura > 1.5 AND largura < 10),
	CONSTRAINT comprimento_valido CHECK (comprimento > 1.5 AND comprimento < 10),
	FOREIGN KEY (cpf_proprietario)
		REFERENCES proprietario(cpf_usuario)
		ON DELETE SET NULL
		ON UPDATE CASCADE
);

CREATE TABLE solicitacao (
	id_solicitacao SERIAL PRIMARY KEY, 
	cpf_motorista CHAR(11),
	id_vaga INT,
	inicio TIMESTAMP NOT NULL,
	fim TIMESTAMP NOT NULL,
	resposta BOOLEAN,
    CONSTRAINT periodo_valido CHECK (fim >= inicio + interval '10' minute AND fim < inicio + interval '24' hour),
	FOREIGN KEY (cpf_motorista)
		REFERENCES motorista(cpf_usuario)
		ON DELETE SET NULL
		ON UPDATE CASCADE,
    FOREIGN KEY (id_vaga)
		REFERENCES vaga(id_vaga)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
	UNIQUE (cpf_motorista, inicio, fim)
);

CREATE TABLE acordo (
	id_acordo SERIAL PRIMARY KEY,
	id_solicitacao INT UNIQUE,
	FOREIGN KEY (id_solicitacao)
		REFERENCES solicitacao(id_solicitacao)
		ON DELETE RESTRICT
		ON UPDATE CASCADE
);


CREATE OR REPLACE FUNCTION checa_perfil_do_novo_agente()
  RETURNS trigger AS $checa_perfil_do_novo_agente$
BEGIN
	IF EXISTS(SELECT 1
               FROM motorista AS m
               WHERE m.cpf_usuario = NEW.cpf_usuario) OR EXISTS(SELECT 1
               FROM proprietario AS p
               WHERE P.cpf_usuario = NEW.cpf_usuario)  THEN
          RAISE EXCEPTION 'Já existe um motorista ou proprietário com esse CPF';
          ROLLBACK;
    END IF;
	RETURN NEW;
END;
$checa_perfil_do_novo_agente$ LANGUAGE plpgsql;

CREATE TRIGGER checa_perfis_usuario
AFTER INSERT
ON agente_municipal
FOR EACH ROW
EXECUTE PROCEDURE checa_perfil_do_novo_agente();


CREATE OR REPLACE FUNCTION checa_perfil_do_proprietario()
  RETURNS trigger AS $checa_perfil_do_proprietario$
BEGIN
	IF EXISTS(SELECT 1
               FROM agente_municipal AS a
               WHERE a.cpf_usuario = NEW.cpf_usuario) THEN
          RAISE EXCEPTION 'Já existe um agente com esse CPF';
          ROLLBACK;
    END IF;
	RETURN NEW;
END;
$checa_perfil_do_proprietario$ LANGUAGE plpgsql;

CREATE TRIGGER checa_perfis_usuario
AFTER INSERT
ON proprietario
FOR EACH ROW
EXECUTE PROCEDURE checa_perfil_do_proprietario();


CREATE OR REPLACE FUNCTION checa_perfil_do_motorista()
  RETURNS trigger AS $checa_perfil_do_motorista$
BEGIN
	IF EXISTS(SELECT 1
               FROM agente_municipal AS a
               WHERE a.cpf_usuario = NEW.cpf_usuario) THEN
          RAISE EXCEPTION 'Já existe um agente com esse CPF';
          ROLLBACK;
    END IF;
	RETURN NEW;
END;
$checa_perfil_do_motorista$ LANGUAGE plpgsql;

CREATE TRIGGER checa_perfis_usuario
AFTER INSERT
ON motorista
FOR EACH ROW
EXECUTE PROCEDURE checa_perfil_do_motorista();


INSERT INTO usuario VALUES ('12345678901', 'Lucas Civile', 'lucas@usp.br', 'lucas123', '1999-11-05');
INSERT INTO usuario VALUES ('12345678902', 'Eduardo Freire', 'eduardo@usp.br', 'eduardo123', '1992-11-28');
INSERT INTO usuario VALUES ('12345678903', 'Giovanni di Luca', 'giovanni@usp.br', 'giovanni123', '1995-08-07');
INSERT INTO usuario VALUES ('12345678904', 'Kelly Braghetto', 'kelly@usp.br', 'kelly123', '1990-05-05');

INSERT INTO proprietario VALUES ('12345678901', 'Avenida Paulista', '1000', 'Apto 123', '01310100');
INSERT INTO proprietario VALUES ('12345678903', 'Rua do Matão', '1010', null, '05508090');
INSERT INTO motorista VALUES ('12345678903', '65748485859');
INSERT INTO motorista VALUES ('12345678902', '09876543210');
INSERT INTO agente_municipal VALUES ('12345678904', '98765');

INSERT INTO veiculo VALUES ('ABC1234', '12345678902', 'Ferrari 458', 2020, 'Vermelho');
INSERT INTO veiculo VALUES ('DEF5678', '12345678902', 'Lamborghini Gallardo', 2010, 'Preto');
INSERT INTO veiculo VALUES ('GHI9012', '12345678903', 'BMW i8', 2019, 'Branco');

INSERT INTO vaga VALUES (DEFAULT, '12345678901', 10, -12.34, 43.21, 6.29, 3.82, TRUE);
INSERT INTO vaga VALUES (DEFAULT, '12345678901', 130.30, -12.35, 53.21, null, null, TRUE);
INSERT INTO vaga VALUES (DEFAULT, '12345678903', 12.99, 98.76, -67.89, 5.0, 9.84, TRUE);

INSERT INTO solicitacao VALUES (DEFAULT, '12345678902', 3, '2020-06-04 04:50:00', '2020-06-04 05:50:00', FALSE);
INSERT INTO solicitacao VALUES (DEFAULT, '12345678902', 1, '2020-05-10 17:48:00', '2020-05-10 18:02:00', TRUE);
INSERT INTO solicitacao VALUES (DEFAULT, '12345678903', 2, '2020-08-23 13:28:00', '2020-08-23 13:58:00');
INSERT INTO solicitacao VALUES (DEFAULT, '12345678903', 1, '2019-08-19 15:10:00', '2019-08-19 16:00:00', TRUE);

INSERT INTO acordo VALUES (DEFAULT, 2);
INSERT INTO acordo VALUES (DEFAULT, 4);
