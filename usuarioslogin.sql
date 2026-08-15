BEGIN;

-- ============================================================
-- PESSOA 1 — ADMIN
-- Professor + Almoxarife + Financeiro
-- NÃO é aluno
-- ============================================================

UPDATE pessoa
SET
    is_admin = TRUE,
    google_id = NULL,
    nome = 'Usuario Admin',             -- Modificar Nome (opcional)
    email = 'admin@universitas.edu.br', -- Modificar Email (obrigatorio)
    telefone = '11999999991'            -- Modificar Telefone (opcional)
WHERE id = 1;


-- Garante que o Admin seja Professor no Campus 1
INSERT INTO professor (pessoa_id, campus_id)
VALUES (1, 1)
ON CONFLICT (pessoa_id)
DO UPDATE SET campus_id = 1;


-- Garante que o Admin seja Almoxarife no Campus 1
INSERT INTO almoxarife (pessoa_id, campus_id)
VALUES (1, 1)
ON CONFLICT (pessoa_id)
DO UPDATE SET campus_id = 1;


-- Garante que o Admin seja Financeiro no Campus 1
INSERT INTO financeiro (pessoa_id, campus_id)
VALUES (1, 1)
ON CONFLICT (pessoa_id)
DO UPDATE SET campus_id = 1;


-- Garante que o Admin NÃO seja aluno
DELETE FROM aluno
WHERE pessoa_id = 1;


-- ============================================================
-- PESSOA 2 — PROFESSOR
-- ============================================================

UPDATE pessoa
SET
    is_admin = FALSE,
    google_id = NULL,
    nome = 'Usuario Professor',             -- Modificar Nome (opcional)
    email = 'professor@universitas.edu.br', -- Modificar Email (obrigatorio)
    telefone = '11999999992'                -- Modificar Telefone (opcional)
WHERE id = 2;


INSERT INTO professor (pessoa_id, campus_id)
VALUES (2, 1)
ON CONFLICT (pessoa_id)
DO UPDATE SET campus_id = 1;


-- Garante que não possua outras funções
DELETE FROM aluno
WHERE pessoa_id = 2;

DELETE FROM almoxarife
WHERE pessoa_id = 2;

DELETE FROM financeiro
WHERE pessoa_id = 2;


-- ============================================================
-- PESSOA 3 — ALUNO
-- ============================================================

UPDATE pessoa
SET
    is_admin = FALSE,
    google_id = NULL,
    nome = 'Usuario Aluno',             -- Modificar Nome (opcional)
    email = 'aluno@universitas.edu.br', -- Modificar Email (obrigatorio)
    telefone = '11999999993'            -- Modificar Telefone (opcional)
WHERE id = 3;


-- Remove possíveis funções administrativas
DELETE FROM professor
WHERE pessoa_id = 3;

DELETE FROM almoxarife
WHERE pessoa_id = 3;

DELETE FROM financeiro
WHERE pessoa_id = 3;


-- Garante que seja aluno no Campus 1
INSERT INTO aluno
    (pessoa_id, matricula, media_geral, coef_rend, campus_id, curso_id, status)
VALUES
    (3, 20261001, 0, 0, 1, 1, 'ATIVO')
ON CONFLICT (pessoa_id)
DO UPDATE SET
    campus_id = 1,
    curso_id = 1;


-- ============================================================
-- PESSOA 4 — FINANCEIRO
-- ============================================================

UPDATE pessoa
SET
    is_admin = FALSE,
    google_id = NULL,
    nome = 'Usuario Financeiro',            -- Modificar Nome (opcional)
    email = 'financeiro@universitas.edu.br',-- Modificar Email (obrigatorio)
    telefone = '11999999994'                -- Modificar Telefone (opcional)
WHERE id = 4;


INSERT INTO financeiro (pessoa_id, campus_id)
VALUES (4, 1)
ON CONFLICT (pessoa_id)
DO UPDATE SET campus_id = 1;


-- Garante que não possua outras funções
DELETE FROM aluno
WHERE pessoa_id = 4;

DELETE FROM professor
WHERE pessoa_id = 4;

DELETE FROM almoxarife
WHERE pessoa_id = 4;


COMMIT;