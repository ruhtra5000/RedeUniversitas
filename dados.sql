--
-- PostgreSQL database dump
--

\restrict V4UCFts1SeLBEef8BsdRsjoiZA6LjYzw04CTG4opH2hM3YldbUc09P3KsY095md

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

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
-- Data for Name: campus; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.campus (id, cnpj, nome, email, telefone, reitor_id) FROM stdin;
2	58257039691431	Campus Beta - Saúde	contato@campusbetasaúde.edu.br	11983415796	\N
3	99260963123154	Campus Gama - Exatas	contato@campusgamaexatas.edu.br	11984428914	\N
4	78756007189745	Campus Delta - Humanas	contato@campusdeltahumanas.edu.br	11984213115	\N
5	17150459568320	Campus Epsilon - Artes	contato@campusepsilonartes.edu.br	11981548511	\N
6	69612575332131	Campus Zeta - Esportes	contato@campuszetaesportes.edu.br	11984641923	\N
7	10498405557549	Campus Eta - Negócios	contato@campusetanegócios.edu.br	11985596150	\N
8	28411541762509	Campus Theta - Agrárias	contato@campusthetaagrárias.edu.br	11984394880	\N
9	87642021478857	Campus Iota - Engenharias	contato@campusiotaengenharias.edu.br	11987175395	\N
10	11359618742192	Campus Kappa - Direito	contato@campuskappadireito.edu.br	11981876932	\N
11	30980502617322	Campus Lambda - Odonto	contato@campuslambdaodonto.edu.br	11989153486	\N
12	91979626549336	Campus Mu - MedVet	contato@campusmumedvet.edu.br	11989269832	\N
13	70486660487543	Campus Nu - Pedagogia	contato@campusnupedagogia.edu.br	11982138181	\N
14	53383644310494	Campus Xi - Letras	contato@campusxiletras.edu.br	11986117837	\N
15	15617218945329	Campus Omicron - Design	contato@campusomicrondesign.edu.br	11986003042	\N
16	59774817488579	Campus Pi - Arquitetura	contato@campuspiarquitetura.edu.br	11989393286	\N
1	00000000000001	Campus Alpha - Tecnologia	alpha@universitas.edu.br	11988888888	1
\.


--
-- Data for Name: pessoa; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.pessoa (id, google_id, is_admin, cpf, nome, email, telefone) FROM stdin;
1	\N	t	11111111111	Usuario Admin	example1@mail.com	11999999991
2	\N	f	22222222222	Usuario Professor	example2@mail.com	11999999992
3	\N	f	33333333333	Usuario Aluno	example3@mail.com	11999999993
4	\N	f	44444444444	Usuario Financeiro	example4@mail.com	11999999994
5	\N	f	47544673531	Daniel Silva	prof.daniel.silva@universitas.edu.br	11932868828
6	\N	f	26048021673	Henrique Oliveira	prof.henrique.oliveira@universitas.edu.br	11990825067
7	\N	f	68370720873	Rafaela Santos	prof.rafaela.santos@universitas.edu.br	11904265799
8	\N	f	41003814027	Ana Santos	prof.ana.santos@universitas.edu.br	11967827638
9	\N	f	38180332966	Tatiana Silva	prof.tatiana.silva@universitas.edu.br	11996102525
10	\N	f	71076327392	Rafaela Alves	prof.rafaela.alves@universitas.edu.br	11979089901
11	\N	f	13733616459	Isabela Martins	prof.isabela.martins@universitas.edu.br	11921429110
12	\N	f	28373317513	Nicolas Ferreira	prof.nicolas.ferreira@universitas.edu.br	11928898923
13	\N	f	61937947921	Karina Santos	prof.karina.santos@universitas.edu.br	11912981052
14	\N	f	93081657201	Lucas Carvalho	prof.lucas.carvalho@universitas.edu.br	11935503389
15	\N	f	84987658854	Bruno Ribeiro	prof.bruno.ribeiro@universitas.edu.br	11916753883
16	\N	f	51025702129	Mariana Santos	prof.mariana.santos@universitas.edu.br	11984374605
17	\N	f	60945643201	Tatiana Almeida	prof.tatiana.almeida@universitas.edu.br	11977490893
18	\N	f	14593704402	Gabriela Ribeiro	prof.gabriela.ribeiro@universitas.edu.br	11988753260
19	\N	f	61973405392	Henrique Martins	prof.henrique.martins@universitas.edu.br	11937308985
20	\N	f	60827117278	Olivia Costa	aluno.olivia.costa@universitas.edu.br	11921831063
21	\N	f	21373225387	Lucas Ferreira	aluno.lucas.ferreira@universitas.edu.br	11981756179
22	\N	f	43196346836	Fernando Lima	aluno.fernando.lima@universitas.edu.br	11921931511
23	\N	f	99873870754	Olivia Alves	aluno.olivia.alves@universitas.edu.br	11992363534
24	\N	f	55890068783	Rafaela Souza	aluno.rafaela.souza@universitas.edu.br	11907507864
25	\N	f	62894468092	Henrique Carvalho	aluno.henrique.carvalho@universitas.edu.br	11935935572
26	\N	f	56033091279	Carla Souza	aluno.carla.souza@universitas.edu.br	11928538251
27	\N	f	72890569906	Pedro Alves	aluno.pedro.alves@universitas.edu.br	11919175900
28	\N	f	85425501819	Isabela Oliveira	aluno.isabela.oliveira@universitas.edu.br	11935264581
29	\N	f	91165531253	Samuel Alves	aluno.samuel.alves@universitas.edu.br	11953606628
30	\N	f	79313607044	Lucas Souza	aluno.lucas.souza@universitas.edu.br	11966238574
31	\N	f	27650808629	Carla Martins	aluno.carla.martins@universitas.edu.br	11984214382
32	\N	f	68757219412	Fernando Martins	aluno.fernando.martins@universitas.edu.br	11980048665
33	\N	f	93243420962	Carla Alves	aluno.carla.alves@universitas.edu.br	11962820592
34	\N	f	87185193913	Quintino Rodrigues	aluno.quintino.rodrigues@universitas.edu.br	11901540956
35	\N	f	86814581501	Daniel Costa	aluno.daniel.costa@universitas.edu.br	11935812670
36	\N	f	67095148296	Karina Santos	aluno.karina.santos@universitas.edu.br	11921227574
37	\N	f	79486780724	Olivia Silva	aluno.olivia.silva@universitas.edu.br	11914282218
38	\N	f	81463743911	João Carvalho	aluno.joão.carvalho@universitas.edu.br	11981734598
39	\N	f	83708291861	Gabriela Oliveira	aluno.gabriela.oliveira@universitas.edu.br	11971182864
40	\N	f	75816749115	Ana Gomes	aluno.ana.gomes@universitas.edu.br	11902614124
41	\N	f	52119777069	Daniel Almeida	aluno.daniel.almeida@universitas.edu.br	11932138745
42	\N	f	91080433848	Bruno Souza	aluno.bruno.souza@universitas.edu.br	11910570592
43	\N	f	86281205445	Carla Ribeiro	aluno.carla.ribeiro@universitas.edu.br	11916879290
44	\N	f	33836224944	Eduarda Costa	aluno.eduarda.costa@universitas.edu.br	11935575298
45	\N	f	68439875878	Quintino Carvalho	fin.quintino.carvalho@universitas.edu.br	11928427073
46	\N	f	62878418842	Rafaela Martins	fin.rafaela.martins@universitas.edu.br	11990152297
47	\N	f	82583289803	Lucas Pereira	fin.lucas.pereira@universitas.edu.br	11960597444
48	\N	f	19555002319	Daniel Souza	fin.daniel.souza@universitas.edu.br	11945377076
49	\N	f	42443845891	Ana Gomes	fin.ana.gomes@universitas.edu.br	11978979095
50	\N	f	17005533878	Henrique Silva	fin.henrique.silva@universitas.edu.br	11930728046
51	\N	f	20009114172	Carla Almeida	fin.carla.almeida@universitas.edu.br	11969008866
52	\N	f	77297747111	Henrique Rodrigues	fin.henrique.rodrigues@universitas.edu.br	11928754377
53	\N	f	91099217763	Rafaela Oliveira	fin.rafaela.oliveira@universitas.edu.br	11977337818
54	\N	f	77794424223	Pedro Souza	fin.pedro.souza@universitas.edu.br	11954634663
55	\N	f	59095990995	Gabriela Santos	fin.gabriela.santos@universitas.edu.br	11956851760
56	\N	f	25660222785	Nicolas Pereira	fin.nicolas.pereira@universitas.edu.br	11908135295
57	\N	f	26585757278	Mariana Ribeiro	fin.mariana.ribeiro@universitas.edu.br	11933374088
58	\N	f	72432871908	Gabriela Souza	fin.gabriela.souza@universitas.edu.br	11918814949
59	\N	f	71325884441	Nicolas Oliveira	fin.nicolas.oliveira@universitas.edu.br	11933528453
60	\N	f	86690793838	Carla Pereira	almox.carla.pereira@universitas.edu.br	11913141087
61	\N	f	87306329557	Bruno Costa	almox.bruno.costa@universitas.edu.br	11901980765
62	\N	f	32490078656	Carla Almeida	almox.carla.almeida@universitas.edu.br	11954547971
63	\N	f	31726673616	Pedro Pereira	almox.pedro.pereira@universitas.edu.br	11950864911
64	\N	f	50608951738	Ana Alves	almox.ana.alves@universitas.edu.br	11956775103
65	\N	f	77510049482	Rafaela Costa	almox.rafaela.costa@universitas.edu.br	11920776478
66	\N	f	87560595158	Gabriela Rodrigues	almox.gabriela.rodrigues@universitas.edu.br	11998748972
67	\N	f	56162203547	Rafaela Silva	almox.rafaela.silva@universitas.edu.br	11907672593
68	\N	f	80767267818	Bruno Gomes	almox.bruno.gomes@universitas.edu.br	11971286543
69	\N	f	82845990690	Fernando Silva	almox.fernando.silva@universitas.edu.br	11910752378
70	\N	f	21145590913	Fernando Santos	almox.fernando.santos@universitas.edu.br	11990625494
71	\N	f	91133166233	Henrique Alves	almox.henrique.alves@universitas.edu.br	11933046464
72	\N	f	91775067774	Samuel Gomes	almox.samuel.gomes@universitas.edu.br	11911003626
73	\N	f	89816264716	Nicolas Costa	almox.nicolas.costa@universitas.edu.br	11970166708
74	\N	f	36889783906	Karina Almeida	almox.karina.almeida@universitas.edu.br	11989889098
\.


--
-- Data for Name: almoxarife; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.almoxarife (pessoa_id, campus_id) FROM stdin;
1	1
60	15
61	14
62	9
63	11
64	8
65	3
66	9
67	15
68	8
69	15
70	13
71	11
72	1
73	16
74	11
\.


--
-- Data for Name: professor; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.professor (pessoa_id, campus_id) FROM stdin;
1	1
2	14
5	5
6	8
7	6
8	6
9	14
10	1
11	6
12	11
13	14
14	8
15	9
16	6
17	4
18	13
19	2
\.


--
-- Data for Name: curso; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.curso (id, nome, modalidade, mensalidade_base, carga_horaria, dur_min_semestre, dur_max_semestre, campus_id, coordenador_id) FROM stdin;
1	Ciência da Computação	PRESENCIAL	1500.00	3200	8	12	1	2
2	Sistemas de Informação	PRESENCIAL	2025.25	2456	6	10	9	9
3	Engenharia de Software	PRESENCIAL	4361.38	2943	6	10	4	17
4	Medicina	EAD	3495.62	3042	9	13	4	16
5	Enfermagem	PRESENCIAL	1503.29	2490	9	13	1	10
6	Engenharia Civil	EAD	2395.80	3760	8	12	11	7
7	Engenharia Elétrica	PRESENCIAL	4130.17	3438	8	12	14	14
8	Administração	EAD	3379.67	3535	7	11	7	17
9	Ciências Contábeis	PRESENCIAL	4279.35	3787	7	11	10	16
10	Direito	PRESENCIAL	3884.78	3022	8	12	7	17
11	Psicologia	PRESENCIAL	3044.65	3059	9	13	15	18
12	Arquitetura e Urbanismo	PRESENCIAL	1590.70	3369	7	11	3	13
13	Design Gráfico	PRESENCIAL	3256.26	3668	8	12	3	11
14	Educação Física	PRESENCIAL	1948.55	2807	7	11	1	5
15	Fisioterapia	PRESENCIAL	4440.56	3651	6	10	15	17
16	Nutrição	PRESENCIAL	2929.98	3871	9	13	16	16
17	Farmácia	PRESENCIAL	1346.01	3808	6	10	4	17
\.


--
-- Data for Name: aluno; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.aluno (pessoa_id, matricula, media_geral, coef_rend, campus_id, curso_id) FROM stdin;
3	20261001	0	0	1	1
20	20260020	0	0	9	16
21	20260021	0	0	15	3
22	20260022	0	0	2	14
23	20260023	0	0	11	9
24	20260024	0	0	1	3
25	20260025	0	0	8	1
26	20260026	0	0	9	2
27	20260027	0	0	6	16
28	20260028	0	0	15	9
29	20260029	0	0	6	14
30	20260030	0	0	16	3
31	20260031	0	0	16	12
32	20260032	0	0	14	11
33	20260033	0	0	11	4
34	20260034	0	0	6	11
35	20260035	0	0	14	16
36	20260036	0	0	10	13
37	20260037	0	0	2	15
38	20260038	0	0	3	11
39	20260039	0	0	9	11
40	20260040	0	0	4	13
41	20260041	0	0	1	15
42	20260042	0	0	14	2
43	20260043	0	0	7	12
44	20260044	0	0	16	15
\.


--
-- Data for Name: bolsa; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.bolsa (id, aluno_id, tipo_bolsa, percentual_desconto, data_inicio, data_fim, status) FROM stdin;
\.


--
-- Data for Name: caixa; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.caixa (id, valor_caixa, campus_id) FROM stdin;
1	150000.00	1
2	436366.96	2
3	150095.17	3
4	417463.97	4
5	257136.46	5
6	187335.89	6
7	407905.47	7
8	152417.97	8
9	60649.00	9
10	136908.40	10
11	197717.88	11
12	438958.82	12
13	485100.10	13
14	175606.25	14
15	338666.78	15
16	229855.27	16
\.


--
-- Data for Name: estoque; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.estoque (id, nome, marca, qtde, qtde_min, campus_id) FROM stdin;
1	Projetor Multimídia	Epson	5	2	1
2	Notebook	LG	254	14	12
3	Mesa de Escritório	Faber-Castell	179	18	9
4	Cadeira Ergonômica	Genérica	269	13	3
5	Resma de Papel A4	Logitech	373	27	16
6	Caneta Esferográfica Azul	Logitech	358	31	16
7	Quadro Branco	Intelbras	410	2	3
8	Apagador	Faber-Castell	118	26	8
9	Marcador para Quadro Branco	Faber-Castell	344	38	12
10	Monitor 24 polegadas	Intelbras	288	34	12
11	Mouse Sem Fio	Tramontina	386	36	11
12	Teclado USB	Chamex	364	30	9
13	Cabo HDMI 2m	Faber-Castell	133	15	4
14	Filtro de Linha	Logitech	166	8	6
15	Ar Condicionado 12000 BTUs	Logitech	115	48	16
16	Lâmpada LED	Faber-Castell	375	38	10
\.


--
-- Data for Name: financeiro; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.financeiro (pessoa_id, campus_id) FROM stdin;
1	1
4	1
45	12
46	3
47	11
48	1
49	14
50	16
51	4
52	14
53	12
54	15
55	5
56	14
57	6
58	9
59	16
\.


--
-- Data for Name: fornecedor; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.fornecedor (id, nome, cnpj, email, telefone) FROM stdin;
1	Kalunga S.A.	43283811000150	vendas@kalunga.com.br	1133334444
2	Gimba	54219764332685	contato@gimba.com.br	1134004485
3	Dell	65702571667473	contato@dell.com.br	1132195773
4	Lenovo	74348488506306	contato@lenovo.com.br	1135304573
5	Papelaria Jovem	20213156210779	contato@papelariajovem.com.br	1130156287
6	Livraria Cultura	97421732664103	contato@livrariacultura.com.br	1139445465
7	Tech Store	24074591063373	contato@techstore.com.br	1131229110
8	InfoHouse	39998360717451	contato@infohouse.com.br	1138487336
9	Cadeira & Cia	28641297091759	contato@cadeiraecia.com.br	1135855396
10	Móveis Projetados	19684639568001	contato@móveisprojetados.com.br	1134098412
11	LimpMax	50107991716818	contato@limpmax.com.br	1132646552
12	BrilhaTudo	96085328814950	contato@brilhatudo.com.br	1138874152
13	ArCondicionado BR	88055950105754	contato@arcondicionadobr.com.br	1135022741
14	Editora Saraiva	28901627628997	contato@editorasaraiva.com.br	1134437001
15	Comercial São Paulo	31876644515991	contato@comercialsãopaulo.com.br	1134569244
16	Borrachas e Lápis	95123166973403	contato@borrachaselápis.com.br	1133533779
\.


--
-- Data for Name: compra; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.compra (id, produto_id, qtde, valor_unit, data_compra, data_recebimento, financeiro_id, fornecedor_id) FROM stdin;
1	1	20	30.00	2026-07-15	\N	4	1
2	4	17	151.64	2026-07-20	\N	55	6
3	10	5	355.47	2026-07-20	\N	48	9
4	2	8	278.91	2026-07-20	\N	48	16
5	4	5	289.16	2026-07-20	\N	59	16
6	15	26	96.26	2026-07-20	\N	45	9
7	16	12	411.95	2026-07-20	\N	56	16
8	3	41	316.58	2026-07-20	\N	45	5
9	5	41	474.82	2026-07-20	\N	46	8
10	4	40	383.40	2026-07-20	\N	51	13
11	15	33	152.19	2026-07-20	\N	57	10
12	2	44	480.25	2026-07-20	\N	47	7
13	7	21	331.91	2026-07-20	\N	49	8
14	6	40	42.16	2026-07-20	\N	4	14
15	15	49	298.94	2026-07-20	\N	53	2
16	8	23	354.94	2026-07-20	\N	58	3
17	8	21	394.97	2026-07-20	\N	50	14
18	4	39	116.28	2026-07-20	\N	48	9
19	5	9	34.52	2026-07-20	\N	53	10
20	15	12	237.01	2026-07-20	\N	53	13
\.


--
-- Data for Name: contapagar; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.contapagar (id, descricao, valor, data_vencimento, data_pagamento, compra_id, caixa_id, financeiro_id) FROM stdin;
\.


--
-- Data for Name: mensalidade; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.mensalidade (id, aluno_id, valor, data_inicio, data_vencimento, foi_paga) FROM stdin;
1	3	1500.00	2026-07-01	2026-08-01	f
2	3	2399.98	2026-08-01	2026-09-01	f
3	20	1873.05	2026-08-01	2026-09-01	f
4	21	2702.12	2026-08-01	2026-09-01	t
5	22	572.17	2026-08-01	2026-09-01	t
6	23	1276.88	2026-08-01	2026-09-01	f
7	24	733.02	2026-08-01	2026-09-01	f
8	25	2867.65	2026-08-01	2026-09-01	f
9	26	2831.63	2026-08-01	2026-09-01	f
10	27	1538.73	2026-08-01	2026-09-01	f
11	28	1109.33	2026-08-01	2026-09-01	f
12	29	976.53	2026-08-01	2026-09-01	t
13	30	1190.62	2026-08-01	2026-09-01	f
14	31	2835.62	2026-08-01	2026-09-01	t
15	32	1207.10	2026-08-01	2026-09-01	f
16	33	2663.15	2026-08-01	2026-09-01	f
17	34	1362.81	2026-08-01	2026-09-01	f
18	35	2832.13	2026-08-01	2026-09-01	t
19	36	1929.49	2026-08-01	2026-09-01	f
20	37	609.12	2026-08-01	2026-09-01	f
21	38	1465.20	2026-08-01	2026-09-01	f
22	39	2912.06	2026-08-01	2026-09-01	f
23	40	2674.25	2026-08-01	2026-09-01	t
24	41	1814.88	2026-08-01	2026-09-01	t
25	42	2306.11	2026-08-01	2026-09-01	t
26	43	687.07	2026-08-01	2026-09-01	f
27	44	2058.15	2026-08-01	2026-09-01	t
\.


--
-- Data for Name: contareceber; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.contareceber (id, descricao, valor, data_vencimento, data_pagamento, mensalidade_id, caixa_id, financeiro_id) FROM stdin;
1	Mensalidade Julho/2026 - João	1500.00	2026-08-01	\N	1	1	\N
2	Mensalidade Ago/2026	2399.98	2026-09-01	\N	2	7	\N
3	Mensalidade Ago/2026	1873.05	2026-09-01	\N	3	10	\N
4	Mensalidade Ago/2026	2702.12	2026-09-01	\N	4	16	\N
5	Mensalidade Ago/2026	572.17	2026-09-01	\N	5	8	\N
6	Mensalidade Ago/2026	1276.88	2026-09-01	\N	6	1	\N
7	Mensalidade Ago/2026	733.02	2026-09-01	\N	7	4	\N
8	Mensalidade Ago/2026	2867.65	2026-09-01	\N	8	5	\N
9	Mensalidade Ago/2026	2831.63	2026-09-01	\N	9	10	\N
10	Mensalidade Ago/2026	1538.73	2026-09-01	\N	10	16	\N
11	Mensalidade Ago/2026	1109.33	2026-09-01	\N	11	5	\N
12	Mensalidade Ago/2026	976.53	2026-09-01	\N	12	5	\N
13	Mensalidade Ago/2026	1190.62	2026-09-01	\N	13	14	\N
14	Mensalidade Ago/2026	2835.62	2026-09-01	\N	14	9	\N
15	Mensalidade Ago/2026	1207.10	2026-09-01	\N	15	10	\N
16	Mensalidade Ago/2026	2663.15	2026-09-01	\N	16	15	\N
17	Mensalidade Ago/2026	1362.81	2026-09-01	\N	17	13	\N
18	Mensalidade Ago/2026	2832.13	2026-09-01	\N	18	7	\N
19	Mensalidade Ago/2026	1929.49	2026-09-01	\N	19	8	\N
20	Mensalidade Ago/2026	609.12	2026-09-01	\N	20	16	\N
21	Mensalidade Ago/2026	1465.20	2026-09-01	\N	21	5	\N
22	Mensalidade Ago/2026	2912.06	2026-09-01	\N	22	5	\N
23	Mensalidade Ago/2026	2674.25	2026-09-01	\N	23	15	\N
24	Mensalidade Ago/2026	1814.88	2026-09-01	\N	24	15	\N
25	Mensalidade Ago/2026	2306.11	2026-09-01	\N	25	14	\N
26	Mensalidade Ago/2026	687.07	2026-09-01	\N	26	9	\N
27	Mensalidade Ago/2026	2058.15	2026-09-01	\N	27	13	\N
\.


--
-- Data for Name: disciplina; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.disciplina (id, nome, codigo, carga_horaria, obrigatoria, curso_id) FROM stdin;
1	Algoritmos e Lógica	CC001	60	t	1
2	Banco de Dados	DISC002	45	t	15
3	Engenharia de Software	DISC003	30	t	4
4	Cálculo I	DISC004	90	t	15
5	Cálculo II	DISC005	120	f	15
6	Física I	DISC006	120	f	15
7	Anatomia Humana	DISC007	45	f	15
8	Direito Constitucional	DISC008	60	t	9
9	Teoria da Administração	DISC009	120	f	8
10	Estrutura de Dados	DISC010	60	f	3
11	Inteligência Artificial	DISC011	60	t	9
12	Sistemas Operacionais	DISC012	60	f	3
13	Redes de Computadores	DISC013	45	t	8
14	Microeconomia	DISC014	90	t	7
15	Contabilidade Geral	DISC015	30	f	14
16	Fisiologia	DISC016	60	f	14
17	Cinesiologia	DISC017	30	t	14
18	História da Arte	DISC018	90	t	13
19	Projeto Arquitetônico	DISC019	90	t	12
\.


--
-- Data for Name: turma; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.turma (id, codigo, semestre, curso_id, disciplina_id, professor_id) FROM stdin;
1	T101	2026.1	1	1	2
2	T102	2026.1	13	14	11
3	T103	2026.2	8	9	17
4	T104	2026.2	1	13	14
5	T105	2026.2	6	15	8
6	T106	2025.1	13	1	6
7	T107	2026.2	5	15	9
8	T108	2025.1	9	13	14
9	T109	2025.2	15	11	14
10	T1010	2026.2	9	14	12
11	T1011	2025.1	16	1	5
12	T1012	2026.1	8	3	5
13	T1013	2025.1	8	7	2
14	T1014	2025.2	8	5	19
15	T1015	2025.1	7	15	12
16	T1016	2026.1	6	4	9
17	T1017	2026.1	4	1	13
18	T1018	2026.2	13	7	6
19	T1019	2025.2	4	10	7
20	T1020	2025.1	12	18	17
\.


--
-- Data for Name: matricula; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.matricula (aluno_id, turma_id, disciplina_id, nota1, nota2, nota3, final, media, frequencia_abs, frequencia_rel, aprovacao) FROM stdin;
3	1	1	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
20	11	18	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
21	13	11	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
22	16	18	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
23	2	3	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
24	8	10	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
25	8	3	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
26	14	4	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
27	4	15	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
28	6	10	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
29	1	2	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
30	11	2	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
31	10	12	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
32	12	14	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
33	5	8	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
34	17	14	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
35	19	6	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
36	6	6	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
37	3	13	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
38	20	8	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
39	16	5	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
40	8	15	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
41	9	15	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
42	9	1	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
43	15	10	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
44	18	6	-1.00	-1.00	-1.00	-1.00	0.00	0	100	\N
\.


--
-- Data for Name: movimentacao; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.movimentacao (id, produto_id, pessoa_id, qtde_mov, data, tipo) FROM stdin;
\.


--
-- Data for Name: prerequisito; Type: TABLE DATA; Schema: public; Owner: user_universitas
--

COPY public.prerequisito (disciplina_id, prerequisito_id) FROM stdin;
\.


--
-- Name: bolsa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.bolsa_id_seq', 1, false);


--
-- Name: caixa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.caixa_id_seq', 16, true);


--
-- Name: campus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.campus_id_seq', 16, true);


--
-- Name: compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.compra_id_seq', 20, true);


--
-- Name: contapagar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.contapagar_id_seq', 1, false);


--
-- Name: contareceber_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.contareceber_id_seq', 27, true);


--
-- Name: curso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.curso_id_seq', 17, true);


--
-- Name: disciplina_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.disciplina_id_seq', 19, true);


--
-- Name: estoque_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.estoque_id_seq', 16, true);


--
-- Name: fornecedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.fornecedor_id_seq', 16, true);


--
-- Name: mensalidade_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.mensalidade_id_seq', 27, true);


--
-- Name: movimentacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.movimentacao_id_seq', 1, false);


--
-- Name: pessoa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.pessoa_id_seq', 74, true);


--
-- Name: turma_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_universitas
--

SELECT pg_catalog.setval('public.turma_id_seq', 20, true);


--
-- PostgreSQL database dump complete
--

\unrestrict V4UCFts1SeLBEef8BsdRsjoiZA6LjYzw04CTG4opH2hM3YldbUc09P3KsY095md

