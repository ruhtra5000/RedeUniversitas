--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3
-- Dumped by pg_dump version 17.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: user_universitas
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO user_universitas;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: user_universitas
--

COMMENT ON SCHEMA public IS '';


--
-- Name: modalidadecurso; Type: TYPE; Schema: public; Owner: user_universitas
--

CREATE TYPE public.modalidadecurso AS ENUM (
    'PRESENCIAL',
    'EAD'
);


ALTER TYPE public.modalidadecurso OWNER TO user_universitas;

--
-- Name: statusbolsa; Type: TYPE; Schema: public; Owner: user_universitas
--

CREATE TYPE public.statusbolsa AS ENUM (
    'ATIVA',
    'SUSPENSA',
    'ENCERRADA',
    'CANCELADA'
);


ALTER TYPE public.statusbolsa OWNER TO user_universitas;

--
-- Name: statusmovimentacao; Type: TYPE; Schema: public; Owner: user_universitas
--

CREATE TYPE public.statusmovimentacao AS ENUM (
    'ENTRADA',
    'SAIDA',
    'AJUSTE',
    'PERDA'
);


ALTER TYPE public.statusmovimentacao OWNER TO user_universitas;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: almoxarife; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.almoxarife (
    pessoa_id integer NOT NULL,
    campus_id integer NOT NULL
);


ALTER TABLE public.almoxarife OWNER TO user_universitas;

--
-- Name: aluno; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.aluno (
    pessoa_id integer NOT NULL,
    matricula character varying(25) NOT NULL,
    media_geral double precision NOT NULL,
    coef_rend double precision NOT NULL,
    campus_id integer NOT NULL,
    curso_id integer NOT NULL,
    CONSTRAINT ck_aluno_coef_rend CHECK (((coef_rend >= (0)::double precision) AND (coef_rend <= (10)::double precision))),
    CONSTRAINT ck_aluno_media_geral CHECK (((media_geral >= (0)::double precision) AND (media_geral <= (10)::double precision)))
);


ALTER TABLE public.aluno OWNER TO user_universitas;

--
-- Name: bolsa; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.bolsa (
    id integer NOT NULL,
    aluno_id integer NOT NULL,
    tipo_bolsa character varying(25) NOT NULL,
    percentual_desconto double precision NOT NULL,
    data_inicio date NOT NULL,
    data_fim date NOT NULL,
    status public.statusbolsa NOT NULL,
    CONSTRAINT ck_bolsa_percentual_desconto CHECK (((percentual_desconto >= (0)::double precision) AND (percentual_desconto <= (1)::double precision)))
);


ALTER TABLE public.bolsa OWNER TO user_universitas;

--
-- Name: bolsa_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.bolsa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bolsa_id_seq OWNER TO user_universitas;

--
-- Name: bolsa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.bolsa_id_seq OWNED BY public.bolsa.id;


--
-- Name: caixa; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.caixa (
    id integer NOT NULL,
    valor_caixa numeric(10,2) NOT NULL,
    campus_id integer NOT NULL,
    CONSTRAINT ck_caixa_valor_caixa CHECK ((valor_caixa >= (0)::numeric))
);


ALTER TABLE public.caixa OWNER TO user_universitas;

--
-- Name: caixa_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.caixa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.caixa_id_seq OWNER TO user_universitas;

--
-- Name: caixa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.caixa_id_seq OWNED BY public.caixa.id;


--
-- Name: campus; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.campus (
    id integer NOT NULL,
    cnpj character varying(14) NOT NULL,
    nome character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    telefone character varying(25),
    reitor_id integer
);


ALTER TABLE public.campus OWNER TO user_universitas;

--
-- Name: campus_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.campus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.campus_id_seq OWNER TO user_universitas;

--
-- Name: campus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.campus_id_seq OWNED BY public.campus.id;


--
-- Name: compra; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.compra (
    id integer NOT NULL,
    produto_id integer NOT NULL,
    qtde integer NOT NULL,
    valor_unit numeric(8,2) NOT NULL,
    data_compra date NOT NULL,
    data_recebimento date,
    financeiro_id integer NOT NULL,
    fornecedor_id integer NOT NULL,
    CONSTRAINT ck_compra_qtde CHECK ((qtde >= 1)),
    CONSTRAINT ck_compra_valor_unit CHECK ((valor_unit > (0)::numeric))
);


ALTER TABLE public.compra OWNER TO user_universitas;

--
-- Name: compra_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.compra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.compra_id_seq OWNER TO user_universitas;

--
-- Name: compra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.compra_id_seq OWNED BY public.compra.id;


--
-- Name: contapagar; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.contapagar (
    id integer NOT NULL,
    descricao character varying(50) NOT NULL,
    valor numeric(8,2) NOT NULL,
    data_vencimento date NOT NULL,
    data_pagamento date,
    compra_id integer NOT NULL,
    caixa_id integer NOT NULL,
    financeiro_id integer NOT NULL,
    CONSTRAINT ck_contapagar_valor CHECK ((valor >= (0)::numeric))
);


ALTER TABLE public.contapagar OWNER TO user_universitas;

--
-- Name: contapagar_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.contapagar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contapagar_id_seq OWNER TO user_universitas;

--
-- Name: contapagar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.contapagar_id_seq OWNED BY public.contapagar.id;


--
-- Name: contareceber; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.contareceber (
    id integer NOT NULL,
    descricao character varying(50) NOT NULL,
    valor numeric(8,2) NOT NULL,
    data_vencimento date NOT NULL,
    data_pagamento date,
    mensalidade_id integer NOT NULL,
    caixa_id integer NOT NULL,
    financeiro_id integer,
    CONSTRAINT ck_contareceber_valor CHECK ((valor >= (0)::numeric))
);


ALTER TABLE public.contareceber OWNER TO user_universitas;

--
-- Name: contareceber_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.contareceber_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.contareceber_id_seq OWNER TO user_universitas;

--
-- Name: contareceber_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.contareceber_id_seq OWNED BY public.contareceber.id;


--
-- Name: curso; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.curso (
    id integer NOT NULL,
    nome character varying(50) NOT NULL,
    modalidade public.modalidadecurso NOT NULL,
    mensalidade_base numeric(8,2) NOT NULL,
    carga_horaria integer NOT NULL,
    dur_min_semestre integer NOT NULL,
    dur_max_semestre integer NOT NULL,
    campus_id integer NOT NULL,
    coordenador_id integer,
    CONSTRAINT ck_curso_mensalidade_base CHECK ((mensalidade_base > (0)::numeric))
);


ALTER TABLE public.curso OWNER TO user_universitas;

--
-- Name: curso_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.curso_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.curso_id_seq OWNER TO user_universitas;

--
-- Name: curso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.curso_id_seq OWNED BY public.curso.id;


--
-- Name: disciplina; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.disciplina (
    id integer NOT NULL,
    nome character varying(50) NOT NULL,
    codigo character varying(25) NOT NULL,
    carga_horaria integer NOT NULL,
    obrigatoria boolean NOT NULL,
    curso_id integer NOT NULL
);


ALTER TABLE public.disciplina OWNER TO user_universitas;

--
-- Name: disciplina_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.disciplina_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.disciplina_id_seq OWNER TO user_universitas;

--
-- Name: disciplina_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.disciplina_id_seq OWNED BY public.disciplina.id;


--
-- Name: estoque; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.estoque (
    id integer NOT NULL,
    nome character varying(50) NOT NULL,
    marca character varying(50) NOT NULL,
    qtde integer NOT NULL,
    qtde_min integer NOT NULL,
    campus_id integer NOT NULL,
    CONSTRAINT ck_estoque_qtde CHECK ((qtde >= 0)),
    CONSTRAINT ck_estoque_qtde_min CHECK ((qtde_min >= 0))
);


ALTER TABLE public.estoque OWNER TO user_universitas;

--
-- Name: estoque_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.estoque_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.estoque_id_seq OWNER TO user_universitas;

--
-- Name: estoque_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.estoque_id_seq OWNED BY public.estoque.id;


--
-- Name: financeiro; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.financeiro (
    pessoa_id integer NOT NULL,
    campus_id integer NOT NULL
);


ALTER TABLE public.financeiro OWNER TO user_universitas;

--
-- Name: fornecedor; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.fornecedor (
    id integer NOT NULL,
    nome character varying(50) NOT NULL,
    cnpj character varying(14) NOT NULL,
    email character varying(50) NOT NULL,
    telefone character varying(25) NOT NULL
);


ALTER TABLE public.fornecedor OWNER TO user_universitas;

--
-- Name: fornecedor_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.fornecedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fornecedor_id_seq OWNER TO user_universitas;

--
-- Name: fornecedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.fornecedor_id_seq OWNED BY public.fornecedor.id;


--
-- Name: matricula; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.matricula (
    aluno_id integer NOT NULL,
    turma_id integer NOT NULL,
    disciplina_id integer NOT NULL,
    nota1 numeric(4,2),
    nota2 numeric(4,2),
    nota3 numeric(4,2),
    final numeric(4,2),
    media numeric(4,2) NOT NULL,
    frequencia_abs integer NOT NULL,
    frequencia_rel double precision NOT NULL,
    aprovacao boolean,
    CONSTRAINT ck_matricula_final CHECK (((final = ('-1'::integer)::numeric) OR ((final >= (0)::numeric) AND (final <= (10)::numeric)))),
    CONSTRAINT ck_matricula_media CHECK (((media >= (0)::numeric) AND (media <= (10)::numeric))),
    CONSTRAINT ck_matricula_nota1 CHECK (((nota1 = ('-1'::integer)::numeric) OR ((nota1 >= (0)::numeric) AND (nota1 <= (10)::numeric)))),
    CONSTRAINT ck_matricula_nota2 CHECK (((nota2 = ('-1'::integer)::numeric) OR ((nota2 >= (0)::numeric) AND (nota2 <= (10)::numeric)))),
    CONSTRAINT ck_matricula_nota3 CHECK (((nota3 = ('-1'::integer)::numeric) OR ((nota3 >= (0)::numeric) AND (nota3 <= (10)::numeric))))
);


ALTER TABLE public.matricula OWNER TO user_universitas;

--
-- Name: mensalidade; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.mensalidade (
    id integer NOT NULL,
    aluno_id integer NOT NULL,
    valor numeric(8,2) NOT NULL,
    data_inicio date NOT NULL,
    data_vencimento date NOT NULL,
    foi_paga boolean NOT NULL,
    CONSTRAINT ck_mensalidade_valor CHECK ((valor >= (0)::numeric))
);


ALTER TABLE public.mensalidade OWNER TO user_universitas;

--
-- Name: mensalidade_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.mensalidade_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mensalidade_id_seq OWNER TO user_universitas;

--
-- Name: mensalidade_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.mensalidade_id_seq OWNED BY public.mensalidade.id;


--
-- Name: movimentacao; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.movimentacao (
    id integer NOT NULL,
    produto_id integer NOT NULL,
    pessoa_id integer NOT NULL,
    qtde_mov integer NOT NULL,
    data timestamp without time zone NOT NULL,
    tipo public.statusmovimentacao NOT NULL,
    CONSTRAINT ck_movimentacao_qtde_mov CHECK ((qtde_mov > 0))
);


ALTER TABLE public.movimentacao OWNER TO user_universitas;

--
-- Name: movimentacao_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.movimentacao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.movimentacao_id_seq OWNER TO user_universitas;

--
-- Name: movimentacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.movimentacao_id_seq OWNED BY public.movimentacao.id;


--
-- Name: pessoa; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.pessoa (
    id integer NOT NULL,
    google_id character varying(100),
    is_admin boolean NOT NULL,
    cpf character varying(11) NOT NULL,
    nome character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    telefone character varying(25)
);


ALTER TABLE public.pessoa OWNER TO user_universitas;

--
-- Name: pessoa_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.pessoa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pessoa_id_seq OWNER TO user_universitas;

--
-- Name: pessoa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.pessoa_id_seq OWNED BY public.pessoa.id;


--
-- Name: prerequisito; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.prerequisito (
    disciplina_id integer NOT NULL,
    prerequisito_id integer NOT NULL
);


ALTER TABLE public.prerequisito OWNER TO user_universitas;

--
-- Name: professor; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.professor (
    pessoa_id integer NOT NULL,
    campus_id integer NOT NULL
);


ALTER TABLE public.professor OWNER TO user_universitas;

--
-- Name: turma; Type: TABLE; Schema: public; Owner: user_universitas
--

CREATE TABLE public.turma (
    id integer NOT NULL,
    codigo character varying(25) NOT NULL,
    semestre character varying(25) NOT NULL,
    curso_id integer NOT NULL,
    disciplina_id integer NOT NULL,
    professor_id integer NOT NULL
);


ALTER TABLE public.turma OWNER TO user_universitas;

--
-- Name: turma_id_seq; Type: SEQUENCE; Schema: public; Owner: user_universitas
--

CREATE SEQUENCE public.turma_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.turma_id_seq OWNER TO user_universitas;

--
-- Name: turma_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_universitas
--

ALTER SEQUENCE public.turma_id_seq OWNED BY public.turma.id;


--
-- Name: bolsa id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.bolsa ALTER COLUMN id SET DEFAULT nextval('public.bolsa_id_seq'::regclass);


--
-- Name: caixa id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.caixa ALTER COLUMN id SET DEFAULT nextval('public.caixa_id_seq'::regclass);


--
-- Name: campus id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.campus ALTER COLUMN id SET DEFAULT nextval('public.campus_id_seq'::regclass);


--
-- Name: compra id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.compra ALTER COLUMN id SET DEFAULT nextval('public.compra_id_seq'::regclass);


--
-- Name: contapagar id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.contapagar ALTER COLUMN id SET DEFAULT nextval('public.contapagar_id_seq'::regclass);


--
-- Name: contareceber id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.contareceber ALTER COLUMN id SET DEFAULT nextval('public.contareceber_id_seq'::regclass);


--
-- Name: curso id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.curso ALTER COLUMN id SET DEFAULT nextval('public.curso_id_seq'::regclass);


--
-- Name: disciplina id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.disciplina ALTER COLUMN id SET DEFAULT nextval('public.disciplina_id_seq'::regclass);


--
-- Name: estoque id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.estoque ALTER COLUMN id SET DEFAULT nextval('public.estoque_id_seq'::regclass);


--
-- Name: fornecedor id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.fornecedor ALTER COLUMN id SET DEFAULT nextval('public.fornecedor_id_seq'::regclass);


--
-- Name: mensalidade id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.mensalidade ALTER COLUMN id SET DEFAULT nextval('public.mensalidade_id_seq'::regclass);


--
-- Name: movimentacao id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.movimentacao ALTER COLUMN id SET DEFAULT nextval('public.movimentacao_id_seq'::regclass);


--
-- Name: pessoa id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.pessoa ALTER COLUMN id SET DEFAULT nextval('public.pessoa_id_seq'::regclass);


--
-- Name: turma id; Type: DEFAULT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.turma ALTER COLUMN id SET DEFAULT nextval('public.turma_id_seq'::regclass);


--
-- Name: almoxarife almoxarife_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.almoxarife
    ADD CONSTRAINT almoxarife_pkey PRIMARY KEY (pessoa_id);


--
-- Name: aluno aluno_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.aluno
    ADD CONSTRAINT aluno_pkey PRIMARY KEY (pessoa_id);


--
-- Name: bolsa bolsa_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.bolsa
    ADD CONSTRAINT bolsa_pkey PRIMARY KEY (id);


--
-- Name: caixa caixa_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.caixa
    ADD CONSTRAINT caixa_pkey PRIMARY KEY (id);


--
-- Name: campus campus_cnpj_key; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.campus
    ADD CONSTRAINT campus_cnpj_key UNIQUE (cnpj);


--
-- Name: campus campus_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.campus
    ADD CONSTRAINT campus_pkey PRIMARY KEY (id);


--
-- Name: compra compra_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.compra
    ADD CONSTRAINT compra_pkey PRIMARY KEY (id);


--
-- Name: contapagar contapagar_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.contapagar
    ADD CONSTRAINT contapagar_pkey PRIMARY KEY (id);


--
-- Name: contareceber contareceber_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.contareceber
    ADD CONSTRAINT contareceber_pkey PRIMARY KEY (id);


--
-- Name: curso curso_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.curso
    ADD CONSTRAINT curso_pkey PRIMARY KEY (id);


--
-- Name: disciplina disciplina_codigo_key; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.disciplina
    ADD CONSTRAINT disciplina_codigo_key UNIQUE (codigo);


--
-- Name: disciplina disciplina_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.disciplina
    ADD CONSTRAINT disciplina_pkey PRIMARY KEY (id);


--
-- Name: estoque estoque_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.estoque
    ADD CONSTRAINT estoque_pkey PRIMARY KEY (id);


--
-- Name: financeiro financeiro_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.financeiro
    ADD CONSTRAINT financeiro_pkey PRIMARY KEY (pessoa_id);


--
-- Name: fornecedor fornecedor_cnpj_key; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.fornecedor
    ADD CONSTRAINT fornecedor_cnpj_key UNIQUE (cnpj);


--
-- Name: fornecedor fornecedor_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.fornecedor
    ADD CONSTRAINT fornecedor_pkey PRIMARY KEY (id);


--
-- Name: matricula matricula_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.matricula
    ADD CONSTRAINT matricula_pkey PRIMARY KEY (aluno_id, turma_id);


--
-- Name: mensalidade mensalidade_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.mensalidade
    ADD CONSTRAINT mensalidade_pkey PRIMARY KEY (id);


--
-- Name: movimentacao movimentacao_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.movimentacao
    ADD CONSTRAINT movimentacao_pkey PRIMARY KEY (id);


--
-- Name: pessoa pessoa_cpf_key; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.pessoa
    ADD CONSTRAINT pessoa_cpf_key UNIQUE (cpf);


--
-- Name: pessoa pessoa_email_key; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.pessoa
    ADD CONSTRAINT pessoa_email_key UNIQUE (email);


--
-- Name: pessoa pessoa_google_id_key; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.pessoa
    ADD CONSTRAINT pessoa_google_id_key UNIQUE (google_id);


--
-- Name: pessoa pessoa_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.pessoa
    ADD CONSTRAINT pessoa_pkey PRIMARY KEY (id);


--
-- Name: pessoa pessoa_telefone_key; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.pessoa
    ADD CONSTRAINT pessoa_telefone_key UNIQUE (telefone);


--
-- Name: prerequisito prerequisito_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.prerequisito
    ADD CONSTRAINT prerequisito_pkey PRIMARY KEY (disciplina_id, prerequisito_id);


--
-- Name: professor professor_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.professor
    ADD CONSTRAINT professor_pkey PRIMARY KEY (pessoa_id);


--
-- Name: turma turma_pkey; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.turma
    ADD CONSTRAINT turma_pkey PRIMARY KEY (id);


--
-- Name: aluno uq_aluno_campus_matricula; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.aluno
    ADD CONSTRAINT uq_aluno_campus_matricula UNIQUE (campus_id, matricula);


--
-- Name: disciplina uq_disciplina_curso_nome; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.disciplina
    ADD CONSTRAINT uq_disciplina_curso_nome UNIQUE (curso_id, nome);


--
-- Name: turma uq_turma_codigo_semestre; Type: CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.turma
    ADD CONSTRAINT uq_turma_codigo_semestre UNIQUE (codigo, semestre);


--
-- Name: uq_bolsa_ativa; Type: INDEX; Schema: public; Owner: user_universitas
--

CREATE UNIQUE INDEX uq_bolsa_ativa ON public.bolsa USING btree (aluno_id) WHERE (status = 'ATIVA'::public.statusbolsa);


--
-- Name: almoxarife almoxarife_campus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.almoxarife
    ADD CONSTRAINT almoxarife_campus_id_fkey FOREIGN KEY (campus_id) REFERENCES public.campus(id);


--
-- Name: almoxarife almoxarife_pessoa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.almoxarife
    ADD CONSTRAINT almoxarife_pessoa_id_fkey FOREIGN KEY (pessoa_id) REFERENCES public.pessoa(id);


--
-- Name: aluno aluno_campus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.aluno
    ADD CONSTRAINT aluno_campus_id_fkey FOREIGN KEY (campus_id) REFERENCES public.campus(id);


--
-- Name: aluno aluno_curso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.aluno
    ADD CONSTRAINT aluno_curso_id_fkey FOREIGN KEY (curso_id) REFERENCES public.curso(id);


--
-- Name: aluno aluno_pessoa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.aluno
    ADD CONSTRAINT aluno_pessoa_id_fkey FOREIGN KEY (pessoa_id) REFERENCES public.pessoa(id);


--
-- Name: bolsa bolsa_aluno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.bolsa
    ADD CONSTRAINT bolsa_aluno_id_fkey FOREIGN KEY (aluno_id) REFERENCES public.aluno(pessoa_id);


--
-- Name: caixa caixa_campus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.caixa
    ADD CONSTRAINT caixa_campus_id_fkey FOREIGN KEY (campus_id) REFERENCES public.campus(id);


--
-- Name: campus campus_reitor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.campus
    ADD CONSTRAINT campus_reitor_id_fkey FOREIGN KEY (reitor_id) REFERENCES public.professor(pessoa_id);


--
-- Name: compra compra_financeiro_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.compra
    ADD CONSTRAINT compra_financeiro_id_fkey FOREIGN KEY (financeiro_id) REFERENCES public.financeiro(pessoa_id);


--
-- Name: compra compra_fornecedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.compra
    ADD CONSTRAINT compra_fornecedor_id_fkey FOREIGN KEY (fornecedor_id) REFERENCES public.fornecedor(id);


--
-- Name: compra compra_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.compra
    ADD CONSTRAINT compra_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.estoque(id);


--
-- Name: contapagar contapagar_caixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.contapagar
    ADD CONSTRAINT contapagar_caixa_id_fkey FOREIGN KEY (caixa_id) REFERENCES public.caixa(id);


--
-- Name: contapagar contapagar_compra_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.contapagar
    ADD CONSTRAINT contapagar_compra_id_fkey FOREIGN KEY (compra_id) REFERENCES public.compra(id);


--
-- Name: contapagar contapagar_financeiro_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.contapagar
    ADD CONSTRAINT contapagar_financeiro_id_fkey FOREIGN KEY (financeiro_id) REFERENCES public.financeiro(pessoa_id);


--
-- Name: contareceber contareceber_caixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.contareceber
    ADD CONSTRAINT contareceber_caixa_id_fkey FOREIGN KEY (caixa_id) REFERENCES public.caixa(id);


--
-- Name: contareceber contareceber_financeiro_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.contareceber
    ADD CONSTRAINT contareceber_financeiro_id_fkey FOREIGN KEY (financeiro_id) REFERENCES public.financeiro(pessoa_id);


--
-- Name: contareceber contareceber_mensalidade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.contareceber
    ADD CONSTRAINT contareceber_mensalidade_id_fkey FOREIGN KEY (mensalidade_id) REFERENCES public.mensalidade(id);


--
-- Name: curso curso_campus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.curso
    ADD CONSTRAINT curso_campus_id_fkey FOREIGN KEY (campus_id) REFERENCES public.campus(id);


--
-- Name: curso curso_coordenador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.curso
    ADD CONSTRAINT curso_coordenador_id_fkey FOREIGN KEY (coordenador_id) REFERENCES public.professor(pessoa_id);


--
-- Name: disciplina disciplina_curso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.disciplina
    ADD CONSTRAINT disciplina_curso_id_fkey FOREIGN KEY (curso_id) REFERENCES public.curso(id);


--
-- Name: estoque estoque_campus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.estoque
    ADD CONSTRAINT estoque_campus_id_fkey FOREIGN KEY (campus_id) REFERENCES public.campus(id);


--
-- Name: financeiro financeiro_campus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.financeiro
    ADD CONSTRAINT financeiro_campus_id_fkey FOREIGN KEY (campus_id) REFERENCES public.campus(id);


--
-- Name: financeiro financeiro_pessoa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.financeiro
    ADD CONSTRAINT financeiro_pessoa_id_fkey FOREIGN KEY (pessoa_id) REFERENCES public.pessoa(id);


--
-- Name: matricula matricula_aluno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.matricula
    ADD CONSTRAINT matricula_aluno_id_fkey FOREIGN KEY (aluno_id) REFERENCES public.aluno(pessoa_id);


--
-- Name: matricula matricula_disciplina_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.matricula
    ADD CONSTRAINT matricula_disciplina_id_fkey FOREIGN KEY (disciplina_id) REFERENCES public.disciplina(id);


--
-- Name: matricula matricula_turma_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.matricula
    ADD CONSTRAINT matricula_turma_id_fkey FOREIGN KEY (turma_id) REFERENCES public.turma(id);


--
-- Name: mensalidade mensalidade_aluno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.mensalidade
    ADD CONSTRAINT mensalidade_aluno_id_fkey FOREIGN KEY (aluno_id) REFERENCES public.aluno(pessoa_id);


--
-- Name: movimentacao movimentacao_pessoa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.movimentacao
    ADD CONSTRAINT movimentacao_pessoa_id_fkey FOREIGN KEY (pessoa_id) REFERENCES public.almoxarife(pessoa_id);


--
-- Name: movimentacao movimentacao_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.movimentacao
    ADD CONSTRAINT movimentacao_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.estoque(id);


--
-- Name: prerequisito prerequisito_disciplina_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.prerequisito
    ADD CONSTRAINT prerequisito_disciplina_id_fkey FOREIGN KEY (disciplina_id) REFERENCES public.disciplina(id);


--
-- Name: prerequisito prerequisito_prerequisito_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.prerequisito
    ADD CONSTRAINT prerequisito_prerequisito_id_fkey FOREIGN KEY (prerequisito_id) REFERENCES public.disciplina(id);


--
-- Name: professor professor_campus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.professor
    ADD CONSTRAINT professor_campus_id_fkey FOREIGN KEY (campus_id) REFERENCES public.campus(id);


--
-- Name: professor professor_pessoa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.professor
    ADD CONSTRAINT professor_pessoa_id_fkey FOREIGN KEY (pessoa_id) REFERENCES public.pessoa(id);


--
-- Name: turma turma_curso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.turma
    ADD CONSTRAINT turma_curso_id_fkey FOREIGN KEY (curso_id) REFERENCES public.curso(id);


--
-- Name: turma turma_disciplina_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.turma
    ADD CONSTRAINT turma_disciplina_id_fkey FOREIGN KEY (disciplina_id) REFERENCES public.disciplina(id);


--
-- Name: turma turma_professor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_universitas
--

ALTER TABLE ONLY public.turma
    ADD CONSTRAINT turma_professor_id_fkey FOREIGN KEY (professor_id) REFERENCES public.professor(pessoa_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: user_universitas
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

