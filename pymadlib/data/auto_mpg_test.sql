--
-- Greenplum Database database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auto_mpg_test; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auto_mpg_test (
    id bigint,
    symboling integer,
    normalized_losses real,
    make text,
    fuel_type text,
    aspiration text,
    num_of_doors text,
    body_style text,
    drive_wheels text,
    engine_location text,
    wheel_base real,
    length real,
    width real,
    height real,
    curb_weight real,
    engine_type text,
    num_of_cylinders text,
    engine_size real,
    fuel_system text,
    bore real,
    stroke real,
    compression_ratio real,
    horsepower real,
    peak_rpm real,
    city_mpg real,
    highway_mpg real,
    price real
) DISTRIBUTED BY (id);


--
-- Data for Name: auto_mpg_test; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auto_mpg_test (id, symboling, normalized_losses, make, fuel_type, aspiration, num_of_doors, body_style, drive_wheels, engine_location, wheel_base, length, width, height, curb_weight, engine_type, num_of_cylinders, engine_size, fuel_system, bore, stroke, compression_ratio, horsepower, peak_rpm, city_mpg, highway_mpg, price) FROM stdin;
31	0	188	bmw	gas	std	two	sedan	rwd	front	101.2	176.8	64.800003	54.299999	2710	ohc	six	164	mpfi	3.3099999	3.1900001	9	121	4250	21	28	20970
25	2	137	honda	gas	std	two	hatchback	fwd	front	86.599998	144.60001	63.900002	50.799999	1713	ohc	four	92	1bbl	2.9100001	3.4100001	9.6000004	58	4800	49	54	6479
19	1	103	nissan	gas	std	four	wagon	fwd	front	94.5	170.2	63.799999	53.5	2037	ohc	four	97	2bbl	3.1500001	3.29	9.3999996	69	5200	31	37	7999
32	-1	90	toyota	gas	std	four	sedan	rwd	front	104.5	187.8	66.5	54.099998	3131	dohc	six	171	mpfi	3.27	3.3499999	9.1999998	156	5200	20	24	15690
13	3	186	porsche	gas	std	two	hatchback	rwd	front	94.5	168.89999	68.300003	50.200001	2778	ohc	four	151	mpfi	3.9400001	3.1099999	9.5	143	5500	19	27	22018
52	0	106	honda	gas	std	two	hatchback	fwd	front	96.5	167.5	65.199997	53.299999	2236	ohc	four	110	1bbl	3.1500001	3.5799999	9	86	5800	27	33	7895
46	0	108	nissan	gas	std	four	wagon	fwd	front	100.4	184.60001	66.5	56.099998	3296	ohcv	six	181	mpfi	3.4300001	3.27	9	152	5200	17	22	14399
40	-1	95	volvo	gas	turbo	four	sedan	rwd	front	109.1	188.8	68.900002	55.5	3062	ohc	four	141	mpfi	3.78	3.1500001	9.5	114	5400	19	25	22625
2	-1	65	toyota	gas	std	four	sedan	fwd	front	102.4	175.60001	66.5	54.900002	2326	ohc	four	122	mpfi	3.3099999	3.54	8.6999998	92	4200	29	34	8948
34	-1	74	volvo	gas	std	four	wagon	rwd	front	104.3	188.8	67.199997	57.5	3042	ohc	four	141	mpfi	3.78	3.1500001	9.5	114	5400	24	28	16515
22	-1	93	mercedes-benz	diesel	turbo	four	sedan	rwd	front	115.6	202.60001	71.699997	56.299999	3770	ohc	five	183	idi	3.5799999	3.6400001	21.5	123	4350	22	25	31600
54	1	168	toyota	gas	std	two	hatchback	rwd	front	94.5	168.7	64	52.599998	2204	ohc	four	98	2bbl	3.1900001	3.03	9	70	4800	29	34	8238
16	1	113	mazda	gas	std	four	sedan	fwd	front	93.099998	166.8	64.199997	54.099998	1950	ohc	four	91	2bbl	3.0799999	3.1500001	9	68	5000	31	38	7395
48	3	256	volkswagen	gas	std	two	hatchback	fwd	front	94.5	165.7	64	51.400002	2221	ohc	four	109	mpfi	3.1900001	3.4000001	8.5	90	5500	24	29	9980
10	0	108	nissan	gas	std	four	sedan	fwd	front	100.4	184.60001	66.5	55.099998	3060	ohcv	six	181	mpfi	3.4300001	3.27	9	152	5200	19	25	13499
4	1	125	mitsubishi	gas	std	four	sedan	fwd	front	96.300003	172.39999	65.400002	51.599998	2365	ohc	four	122	2bbl	3.3499999	3.46	8.5	88	5000	25	32	6989
30	3	194	nissan	gas	std	two	hatchback	rwd	front	91.300003	170.7	67.900002	49.700001	3071	ohcv	six	181	mpfi	3.4300001	3.27	9	160	5200	19	25	17199
24	0	102	subaru	gas	std	four	sedan	fwd	front	97.199997	172	65.400002	52.5	2340	ohcf	four	108	mpfi	3.6199999	2.6400001	9	94	5200	26	32	9960
37	0	188	bmw	gas	std	four	sedan	rwd	front	101.2	176.8	64.800003	54.299999	2765	ohc	six	164	mpfi	3.3099999	3.1900001	9	121	4250	21	28	21105
18	-1	74	volvo	gas	std	four	wagon	rwd	front	104.3	188.8	67.199997	57.5	3034	ohc	four	141	mpfi	3.78	3.1500001	9.5	114	5400	23	28	13415
57	1	148	dodge	gas	std	four	hatchback	fwd	front	93.699997	157.3	63.799999	50.599998	1967	ohc	four	90	2bbl	2.97	3.23	9.3999996	68	5500	31	38	6229
51	2	134	toyota	gas	std	two	hatchback	rwd	front	98.400002	176.2	65.599998	52	2714	ohc	four	146	mpfi	3.6199999	3.5	9.3000002	116	4800	24	30	11549
45	-1	137	mitsubishi	gas	std	four	sedan	fwd	front	96.300003	172.39999	65.400002	51.599998	2403	ohc	four	110	spdi	3.1700001	3.46	7.5	116	5500	23	30	9279
7	1	118	dodge	gas	std	two	hatchback	fwd	front	93.699997	157.3	63.799999	50.799999	1876	ohc	four	90	2bbl	2.97	3.23	9.3999996	68	5500	31	38	6377
39	-2	103	volvo	gas	std	four	sedan	rwd	front	104.3	188.8	67.199997	56.200001	2935	ohc	four	141	mpfi	3.78	3.1500001	9.5	114	5400	24	28	15985
1	2	94	volkswagen	diesel	std	four	sedan	fwd	front	97.300003	171.7	65.5	55.700001	2264	ohc	four	97	idi	3.01	3.4000001	23	52	4800	37	46	7995
33	0	91	toyota	gas	std	four	sedan	fwd	front	95.699997	166.3	64.400002	52.799999	2140	ohc	four	98	2bbl	3.1900001	3.03	9	70	4800	28	34	9258
27	0	115	mazda	gas	std	four	sedan	fwd	front	98.800003	177.8	66.5	55.5	2410	ohc	four	122	2bbl	3.3900001	3.3900001	8.6000004	84	4800	26	32	10245
21	-1	65	toyota	gas	std	four	hatchback	fwd	front	102.4	175.60001	66.5	53.900002	2414	ohc	four	122	mpfi	3.3099999	3.54	8.6999998	92	4200	27	32	9988
53	2	94	volkswagen	gas	std	four	sedan	fwd	front	97.300003	171.7	65.5	55.700001	2300	ohc	four	109	mpfi	3.1900001	3.4000001	10	100	5500	26	32	9995
15	1	129	mazda	gas	std	two	hatchback	fwd	front	98.800003	177.8	66.5	53.700001	2385	ohc	four	122	2bbl	3.3900001	3.3900001	8.6000004	84	4800	26	32	8845
9	2	122	volkswagen	gas	std	two	sedan	fwd	front	97.300003	171.7	65.5	55.700001	2209	ohc	four	109	mpfi	3.1900001	3.4000001	9	85	5250	27	34	7975
3	1	101	honda	gas	std	two	hatchback	fwd	front	93.699997	150	64	52.599998	1956	ohc	four	92	1bbl	2.9100001	3.4100001	9.1999998	76	6000	30	34	7129
29	1	119	plymouth	gas	std	two	hatchback	fwd	front	93.699997	157.3	63.799999	50.799999	1918	ohc	four	90	2bbl	2.97	3.23	9.3999996	68	5500	37	41	5572
42	2	134	toyota	gas	std	two	hardtop	rwd	front	98.400002	176.2	65.599998	52	2540	ohc	four	146	mpfi	3.6199999	3.5	9.3000002	116	4800	24	30	8449
23	-1	65	toyota	gas	std	four	sedan	fwd	front	102.4	175.60001	66.5	54.900002	2414	ohc	four	122	mpfi	3.3099999	3.54	8.6999998	92	4200	27	32	10898
36	0	118	mazda	gas	std	four	sedan	rwd	front	104.9	175	66.099998	54.400002	2670	ohc	four	140	mpfi	3.76	3.1600001	8	120	5000	19	27	18280
56	0	161	peugot	gas	turbo	four	sedan	rwd	front	108	186.7	68.300003	56	3130	l	four	134	mpfi	3.6099999	3.21	7	142	5600	18	24	18150
50	0	85	subaru	gas	std	four	wagon	4wd	front	96.900002	173.60001	65.400002	54.900002	2420	ohcf	four	108	2bbl	3.6199999	2.6400001	9	82	4800	23	29	8013
12	-1	95	volvo	diesel	turbo	four	sedan	rwd	front	109.1	188.8	68.900002	55.5	3217	ohc	six	145	idi	3.01	3.4000001	23	106	4800	26	27	22470
44	1	129	mazda	gas	std	two	hatchback	fwd	front	98.800003	177.8	66.5	53.700001	2385	ohc	four	122	2bbl	3.3900001	3.3900001	8.6000004	84	4800	26	32	10595
6	2	137	honda	gas	std	two	hatchback	fwd	front	86.599998	144.60001	63.900002	50.799999	1819	ohc	four	92	1bbl	2.9100001	3.4100001	9.1999998	76	6000	31	38	6855
38	2	161	mitsubishi	gas	std	two	hatchback	fwd	front	93.699997	157.3	64.400002	50.799999	1918	ohc	four	92	2bbl	2.97	3.23	9.3999996	68	5500	37	41	5389
26	1	119	plymouth	gas	turbo	two	hatchback	fwd	front	93.699997	157.3	63.799999	50.799999	2128	ohc	four	98	spdi	3.03	3.3900001	7.5999999	102	5500	24	30	7957
20	-1	74	plymouth	gas	std	four	wagon	fwd	front	103.3	174.60001	64.599998	59.799999	2535	ohc	four	122	2bbl	3.3499999	3.46	8.5	88	5000	24	30	8921
14	1	168	toyota	gas	std	two	hatchback	rwd	front	94.5	168.7	64	52.599998	2300	dohc	four	98	mpfi	3.24	3.0799999	9.3999996	112	6600	26	29	9538
8	-1	93	mercedes-benz	diesel	turbo	four	wagon	rwd	front	110	190.89999	70.300003	58.700001	3750	ohc	five	183	idi	3.5799999	3.6400001	21.5	123	4350	22	25	28248
47	-1	65	toyota	diesel	turbo	four	sedan	fwd	front	102.4	175.60001	66.5	54.900002	2480	ohc	four	110	idi	3.27	3.3499999	22.5	73	4500	30	33	10698
28	2	192	bmw	gas	std	two	sedan	rwd	front	101.2	176.8	64.800003	54.299999	2395	ohc	four	108	mpfi	3.5	2.8	8.8000002	101	5800	23	29	16430
41	0	161	peugot	gas	std	four	sedan	rwd	front	107.9	186.7	68.400002	56.700001	3075	l	four	120	mpfi	3.46	3.1900001	8.3999996	97	5000	19	24	16630
35	0	81	chevrolet	gas	std	four	sedan	fwd	front	94.5	158.8	63.599998	52	1909	ohc	four	90	2bbl	3.03	3.1099999	9.6000004	70	5400	38	43	6575
55	3	197	toyota	gas	std	two	hatchback	rwd	front	102.9	183.5	67.699997	52	2976	dohc	six	171	mpfi	3.27	3.3499999	9.3000002	161	5200	20	24	16558
17	1	161	mitsubishi	gas	turbo	two	hatchback	fwd	front	93	157.3	63.799999	50.799999	2145	ohc	four	98	spdi	3.03	3.3900001	7.5999999	102	5500	24	30	7689
49	0	85	honda	gas	std	four	sedan	fwd	front	96.5	175.39999	65.199997	54.099998	2304	ohc	four	110	1bbl	3.1500001	3.5799999	9	86	5800	27	33	8845
11	2	122	volkswagen	diesel	std	two	sedan	fwd	front	97.300003	171.7	65.5	55.700001	2261	ohc	four	97	idi	3.01	3.4000001	23	52	4800	37	46	7775
43	0	145	jaguar	gas	std	four	sedan	rwd	front	113	199.60001	69.599998	52.799999	4066	dohc	six	258	mpfi	3.6300001	4.1700001	8.1000004	176	4750	15	19	32250
5	0	78	honda	gas	std	four	wagon	fwd	front	96.5	157.10001	63.900002	58.299999	2024	ohc	four	92	1bbl	2.9200001	3.4100001	9.1999998	76	6000	30	34	7295
\.


--
-- Greenplum Database database dump complete
--

