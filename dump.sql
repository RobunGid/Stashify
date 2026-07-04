--
-- PostgreSQL database dump
--

\restrict dW4HJxy7lG0EACfQBtOT6x4DpPKCb9GVItIXU8hFNS4YH7K8hXhbMTilNUsOBuV

-- Dumped from database version 17.5 (Debian 17.5-1.pgdg130+1)
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
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.alembic_version VALUES ('ddaff6c91202');


--
-- Data for Name: category_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.category_item VALUES ('82ea357a-1b0a-4b7d-a673-06f28e4142a6', 'Articles', '2026-06-12 13:41:10.805873', '2026-06-12 13:41:10.805875');
INSERT INTO public.category_item VALUES ('0ccee0fa-e461-4862-87a7-bcd3725b38aa', 'Video', '2026-06-14 17:31:11.011798', '2026-06-14 17:31:11.011802');


--
-- Data for Name: resource_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.resource_item VALUES ('6faa3fe4-b497-4837-b372-3359569e6224', 'Статья 242', 'Описание статьи', 'pornhub.com', '#tag1 #tag2', false, '82ea357a-1b0a-4b7d-a673-06f28e4142a6', '2026-06-15 16:00:58.138211', '2026-06-15 16:00:58.138214');
INSERT INTO public.resource_item VALUES ('0064f5fe-6d9b-4626-a64f-fa6f14acda2f', 'Статья о кока коле', 'Описание статьи о кока коле', 'ссылка на статью о кока коле', '#tag34 #tag69', false, '82ea357a-1b0a-4b7d-a673-06f28e4142a6', '2026-06-15 16:01:39.230696', '2026-06-15 16:01:39.2307');
INSERT INTO public.resource_item VALUES ('8898234b-7e4b-462a-adbf-70a3a61d6b26', 'статья третий ресурс', 'описание третьей статьи', 'rule34.xxx', '#tag1', false, '82ea357a-1b0a-4b7d-a673-06f28e4142a6', '2026-06-15 20:38:28.243058', '2026-06-15 20:38:28.24306');
INSERT INTO public.resource_item VALUES ('a16f9c31-7aae-47e7-a3df-e53a70890b44', 'статья про четвёртый шкаф', 'книга говно серебряные глаза лучше', 'scottgames.com', '#fnaf #хоррор #обзор', false, '82ea357a-1b0a-4b7d-a673-06f28e4142a6', '2026-06-15 20:41:17.56583', '2026-06-15 20:41:17.565832');
INSERT INTO public.resource_item VALUES ('2b8b0534-46a7-4c9f-a6c6-24b8c921397a', 'blender 5.0 туториал', 'сегодня я научу куб', 'blender.org', '#blender #tutorial', false, '82ea357a-1b0a-4b7d-a673-06f28e4142a6', '2026-06-15 20:46:21.101616', '2026-06-15 20:46:21.101618');
INSERT INTO public.resource_item VALUES ('9fb2ed21-8441-46c4-8693-4a9d244c771e', '6 полезных привычек для праграмиста', '1 - мыться
ахахахахахах', 'metanit.com', '#программирование #coding', false, '82ea357a-1b0a-4b7d-a673-06f28e4142a6', '2026-06-15 20:49:56.775676', '2026-06-15 20:49:56.775678');


--
-- Data for Name: quiz_item; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: quiz_question; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: user_account; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.user_account VALUES ('38889d79-d8ff-4440-935c-12e55063fc99', 1125108151, 'RobunGid', 'admin', '2026-06-12 13:26:28.707123', '2026-06-12 13:26:28.707125');
INSERT INTO public.user_account VALUES ('fc14da3e-f6da-41e7-b35d-a552edf833d9', 5822096548, 'pdfreportgenerator', 'admin', '2026-06-15 16:02:17.384961', '2026-06-15 16:02:17.384962');


--
-- Data for Name: quiz_rating; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: quiz_result; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: resource_favorite; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: resource_image; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.resource_image VALUES ('0fb95a48-067a-4256-93d3-6f04b96dd613', '6faa3fe4-b497-4837-b372-3359569e6224', 'AgACAgIAAxkBAAIWwmowIbToWWpU8f4uZ29x5VPpazm6AAIQIWsbcj-BSYmcFJvvIrAnAQADAgADeAADPAQ', '2026-06-15 16:00:58.144537', '2026-06-15 16:00:58.144538');
INSERT INTO public.resource_image VALUES ('1e7996ca-cfca-4dad-a137-ba6c3a2cbec6', '6faa3fe4-b497-4837-b372-3359569e6224', 'AgACAgIAAxkBAAIWwmowIbToWWpU8f4uZ29x5VPpazm6AAIQIWsbcj-BSYmcFJvvIrAnAQADAgADeAADPAQ', '2026-06-15 16:00:58.148592', '2026-06-15 16:00:58.148593');
INSERT INTO public.resource_image VALUES ('13426ac0-15a3-4b26-a19a-fdf353549887', '6faa3fe4-b497-4837-b372-3359569e6224', 'AgACAgIAAxkBAAIWwmowIbToWWpU8f4uZ29x5VPpazm6AAIQIWsbcj-BSYmcFJvvIrAnAQADAgADeAADPAQ', '2026-06-15 16:00:58.151045', '2026-06-15 16:00:58.151046');
INSERT INTO public.resource_image VALUES ('bec54054-241b-4aca-8e89-b52ae582dcd6', '0064f5fe-6d9b-4626-a64f-fa6f14acda2f', 'AgACAgIAAxkBAAIWwmowIbToWWpU8f4uZ29x5VPpazm6AAIQIWsbcj-BSYmcFJvvIrAnAQADAgADeAADPAQ', '2026-06-15 16:01:39.246705', '2026-06-15 16:01:39.246707');
INSERT INTO public.resource_image VALUES ('75d9c7e3-8305-4c26-a597-c9f52642523e', '0064f5fe-6d9b-4626-a64f-fa6f14acda2f', 'AgACAgIAAxkBAAIWwmowIbToWWpU8f4uZ29x5VPpazm6AAIQIWsbcj-BSYmcFJvvIrAnAQADAgADeAADPAQ', '2026-06-15 16:01:39.256176', '2026-06-15 16:01:39.256177');
INSERT INTO public.resource_image VALUES ('64a7c792-8df3-4aa7-812a-bb821e71a6c7', '8898234b-7e4b-462a-adbf-70a3a61d6b26', 'AgACAgIAAxkBAAIZ4GowYrEJ2dqCaauEeOUCQUw7pLiSAAJ3IGsbtuiBSTvOKd4EM0MjAQADAgADeQADPAQ', '2026-06-15 20:38:28.257873', '2026-06-15 20:38:28.257874');
INSERT INTO public.resource_image VALUES ('154306a6-f1ee-413f-b359-9c842edcec94', '8898234b-7e4b-462a-adbf-70a3a61d6b26', 'AgACAgIAAxkBAAIZ32owYrHM3uW0U4j0WdfkO5lyV9i1AAJ4IGsbtuiBSXc-DqD1DODBAQADAgADeQADPAQ', '2026-06-15 20:38:28.263088', '2026-06-15 20:38:28.263089');
INSERT INTO public.resource_image VALUES ('e0b899a0-01c4-42d4-ad2d-f0a874448476', 'a16f9c31-7aae-47e7-a3df-e53a70890b44', 'AgACAgIAAxkBAAIaLWowY2P5W9r6z2IKjuLwjOuOxd21AAJ9IGsbtuiBSfd9R-FLNpFEAQADAgADbQADPAQ', '2026-06-15 20:41:17.56987', '2026-06-15 20:41:17.569871');
INSERT INTO public.resource_image VALUES ('aed44904-0ce4-4fba-8313-65c2fa6cfc64', 'a16f9c31-7aae-47e7-a3df-e53a70890b44', 'AgACAgIAAxkBAAIaLmowY2M-2itNYx9enm8-SwL7FZYQAAJ-IGsbtuiBSTCvn3LLNMsoAQADAgADbQADPAQ', '2026-06-15 20:41:17.572243', '2026-06-15 20:41:17.572245');
INSERT INTO public.resource_image VALUES ('de7d9d05-11ef-4422-a279-3ae4b2fe417c', '2b8b0534-46a7-4c9f-a6c6-24b8c921397a', 'AgACAgIAAxkBAAIafWowZJSf2vOSZnHmfBl72u2SGA3BAAKAIGsbtuiBSTYYdaX-snWuAQADAgADeAADPAQ', '2026-06-15 20:46:21.109627', '2026-06-15 20:46:21.109629');
INSERT INTO public.resource_image VALUES ('78056f40-6c66-48e0-9be9-95d5d120b9c8', '2b8b0534-46a7-4c9f-a6c6-24b8c921397a', 'AgACAgIAAxkBAAIafGowZJShSacRy8IqRzJwHIoYxJkRAAJ_IGsbtuiBScPr5FfNa1b5AQADAgADeAADPAQ', '2026-06-15 20:46:21.112127', '2026-06-15 20:46:21.112128');
INSERT INTO public.resource_image VALUES ('bad74f55-afdb-44f4-b9b9-03ea6dc9143f', '9fb2ed21-8441-46c4-8693-4a9d244c771e', 'AgACAgIAAxkBAAIamGowZWyjF8jxTQgxkQn1rLsJlCH1AAKDIGsbtuiBSaq8_7rLH0jYAQADAgADbQADPAQ', '2026-06-15 20:49:56.788579', '2026-06-15 20:49:56.788582');
INSERT INTO public.resource_image VALUES ('dab2e796-5c61-4a5e-b66f-7c753510408f', '9fb2ed21-8441-46c4-8693-4a9d244c771e', 'AgACAgIAAxkBAAIal2owZWyHtvvOpxnGNEf9LetnVC6NAAKCIGsbtuiBSfofC4g4nZV-AQADAgADbQADPAQ', '2026-06-15 20:49:56.794997', '2026-06-15 20:49:56.794999');


--
-- Data for Name: resource_rating; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- PostgreSQL database dump complete
--

\unrestrict dW4HJxy7lG0EACfQBtOT6x4DpPKCb9GVItIXU8hFNS4YH7K8hXhbMTilNUsOBuV

