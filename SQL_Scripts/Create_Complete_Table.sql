USE `consumidor`;

CREATE TABLE IF NOT EXISTS `reclamacoes` (
	`Regiao` CHAR(2) NOT NULL,
	`UF` CHAR(2) NOT NULL,
	`Cidade` VARCHAR(100) NOT NULL,
	`Sexo` CHAR(1) NOT NULL,
	`FaixaEtaria` VARCHAR(30) NOT NULL,
	`AnoAbertura` INT(11) NOT NULL,
	`MesAbertura` INT(11) NOT NULL,
	`DataAbertura` CHAR(10) NOT NULL,
	`DataResposta` VARCHAR(10) NULL,
	`DataFinalizacao` VARCHAR(10) NOT NULL,
	`TempoResposta` CHAR(2) NULL,
	`NomeFantasia` VARCHAR(100) NOT NULL,
	`SegmentoMercado` VARCHAR(100) NOT NULL,
	`Area` VARCHAR(100) NOT NULL,
	`Assunto` VARCHAR(250) NOT NULL,
	`GrupoProblema` VARCHAR(150) NOT NULL,
	`Problema` VARCHAR(150) NOT NULL,
	`ComoComprouContratou` VARCHAR(50) NOT NULL,
	`ProcurouEmpresa` CHAR(1) NOT NULL,
	`Respondida` CHAR(1) NOT NULL,
	`Situacao` VARCHAR(50) NOT NULL,
	`AvaliacaoReclamacao` VARCHAR(50) NOT NULL,
	`NotaConsumidor` CHAR(1) NULL
);