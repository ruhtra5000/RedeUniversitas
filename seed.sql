-- !!! RODE O TRUNCATE ANTES !!!
TRUNCATE TABLE caixa, pessoa, campus, curso, turma, disciplina, professor, aluno, financeiro, almoxarife, estoque, bolsa, mensalidade, fornecedor, compra, contareceber, contapagar, movimentacao, prerequisito, matricula RESTART IDENTITY CASCADE;

-- 1. PESSOAS (1 = ADMIN, 2 = PROFESSOR, 3 = ALUNO)
INSERT INTO pessoa (id, cpf, nome, email, telefone, is_admin) VALUES (1, '11111111111', 'Admin', 'guilherme.paes@ufape.edu.br', '11999999991', true);
INSERT INTO pessoa (id, cpf, nome, email, telefone, is_admin) VALUES (2, '22222222222', 'Professor', 'guilhermepaes1717@gmail.com', '11999999992', false);
INSERT INTO pessoa (id, cpf, nome, email, telefone, is_admin) VALUES (3, '33333333333', 'Aluno', 'porcaranha17@gmail.com', '11999999993', false);
INSERT INTO pessoa (id, cpf, nome, email, telefone, is_admin) VALUES (4, '44444444444', 'Carlos Silva (Financeiro)', 'carlos.fin@universitas.edu.br', '11999999994', false);

-- !!! DICA PARA A APRESENTAÇÃO !!!
-- Para logar como ADMIN, rode: UPDATE pessoa SET email = 'seu.email@gmail.com' WHERE id = 1;
-- Para logar como PROFESSOR, rode: UPDATE pessoa SET email = 'seu.email@gmail.com' WHERE id = 2;
-- Para logar como ALUNO, rode: UPDATE pessoa SET email = 'seu.email@gmail.com' WHERE id = 3;

-- 2. FORNECEDOR
INSERT INTO fornecedor (id, nome, cnpj, email, telefone) VALUES (1, 'Kalunga S.A.', '43283811000150', 'vendas@kalunga.com.br', '1133334444');

-- 3. CAMPUS E PROFESSOR
INSERT INTO campus (id, cnpj, nome, email, telefone, reitor_id) VALUES (1, '00000000000001', 'Campus Alpha - Tecnologia', 'alpha@universitas.edu.br', '1188888888', NULL);

-- Admin (1) e Turing (2) são professores
INSERT INTO professor (pessoa_id, campus_id) VALUES (1, 1);
INSERT INTO professor (pessoa_id, campus_id) VALUES (2, 1);

UPDATE campus SET reitor_id = 1 WHERE id = 1;

-- 4. CAIXA
INSERT INTO caixa (id, valor_caixa, campus_id) VALUES (1, 150000.00, 1);

-- 5. CURSO E DISCIPLINA
INSERT INTO curso (id, nome, modalidade, mensalidade_base, carga_horaria, dur_min_semestre, dur_max_semestre, campus_id, coordenador_id) 
VALUES (1, 'Ciência da Computação', 'PRESENCIAL', 1500.00, 3200, 8, 12, 1, 2);

INSERT INTO disciplina (id, nome, codigo, carga_horaria, obrigatoria, curso_id) VALUES (1, 'Algoritmos e Lógica', 'CC001', 60, true, 1);

-- 6. TURMA (T101 da disciplina Algoritmos, lecionada pelo professor Alan Turing [ID 2])
INSERT INTO turma (id, codigo, semestre, curso_id, disciplina_id, professor_id) VALUES (1, 'T101', '2026.1', 1, 1, 2);

-- 7. ALMOXARIFE E FINANCEIRO
INSERT INTO financeiro (pessoa_id, campus_id) VALUES (1, 1);
INSERT INTO almoxarife (pessoa_id, campus_id) VALUES (1, 1);
INSERT INTO financeiro (pessoa_id, campus_id) VALUES (4, 1);

-- 8. ESTOQUE E COMPRAS
INSERT INTO estoque (id, nome, marca, qtde, qtde_min, campus_id) VALUES (1, 'Projetor Multimídia', 'Epson', 5, 2, 1);
INSERT INTO compra (id, produto_id, qtde, valor_unit, data_compra, financeiro_id, fornecedor_id) VALUES (1, 1, 20, 30.00, '2026-07-15', 4, 1);

-- 9. ALUNO E MENSALIDADES
INSERT INTO aluno (pessoa_id, matricula, media_geral, coef_rend, campus_id, curso_id) VALUES (3, '20261001', 0.0, 0.0, 1, 1);
INSERT INTO mensalidade (id, aluno_id, valor, data_inicio, data_vencimento, foi_paga) VALUES (1, 3, 1500.00, '2026-07-01', '2026-08-01', false);
INSERT INTO contareceber (id, descricao, valor, data_vencimento, mensalidade_id, caixa_id) VALUES (1, 'Mensalidade Julho/2026 - João', 1500.00, '2026-08-01', 1, 1); 

-- 10. MATRÍCULA DO ALUNO NA TURMA (Aluno 3 matriculado na turma 1)
-- Inicializamos as notas com -1 (código para "não lançado ainda").
INSERT INTO matricula (aluno_id, turma_id, disciplina_id, nota1, nota2, nota3, final, media, frequencia_abs, frequencia_rel, aprovacao) 
VALUES (3, 1, 1, -1, -1, -1, -1, 0, 0, 100.0, NULL);

-- 11. ATUALIZAR SEQUENCES (Para que o app continue funcionando sem conflito de IDs)
SELECT setval('pessoa_id_seq', (SELECT MAX(id) FROM pessoa));
SELECT setval('fornecedor_id_seq', (SELECT MAX(id) FROM fornecedor));
SELECT setval('campus_id_seq', (SELECT MAX(id) FROM campus));
SELECT setval('caixa_id_seq', (SELECT MAX(id) FROM caixa));
SELECT setval('curso_id_seq', (SELECT MAX(id) FROM curso));
SELECT setval('disciplina_id_seq', (SELECT MAX(id) FROM disciplina));
SELECT setval('turma_id_seq', (SELECT MAX(id) FROM turma));
SELECT setval('estoque_id_seq', (SELECT MAX(id) FROM estoque));
SELECT setval('compra_id_seq', (SELECT MAX(id) FROM compra));
SELECT setval('mensalidade_id_seq', (SELECT MAX(id) FROM mensalidade));
SELECT setval('contareceber_id_seq', (SELECT MAX(id) FROM contareceber));
