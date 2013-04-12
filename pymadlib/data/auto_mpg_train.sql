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
-- Name: auto_mpg_train; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auto_mpg_train (
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
-- Data for Name: auto_mpg_train; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auto_mpg_train (id, symboling, normalized_losses, make, fuel_type, aspiration, num_of_doors, body_style, drive_wheels, engine_location, wheel_base, length, width, height, curb_weight, engine_type, num_of_cylinders, engine_size, fuel_system, bore, stroke, compression_ratio, horsepower, peak_rpm, city_mpg, highway_mpg, price) FROM stdin;
31	3	150	saab	gas	std	two	hatchback	fwd	front	99.099998	186.60001	66.5	56.099998	2707	ohc	four	121	mpfi	2.54	2.0699999	9.3000002	110	5250	21	28	15040
76	1	168	toyota	gas	std	two	sedan	rwd	front	94.5	168.7	64	52.599998	2169	ohc	four	98	2bbl	3.1900001	3.03	9	70	4800	29	34	8058
25	0	91	toyota	gas	std	four	wagon	4wd	front	95.699997	169.7	63.599998	59.099998	3110	ohc	four	92	2bbl	3.05	3.03	9	62	4800	27	32	8778
70	2	94	volkswagen	diesel	turbo	four	sedan	fwd	front	97.300003	171.7	65.5	55.700001	2319	ohc	four	97	idi	3.01	3.4000001	23	68	4500	37	42	9495
19	2	137	honda	gas	std	two	hatchback	fwd	front	86.599998	144.60001	63.900002	50.799999	1819	ohc	four	92	1bbl	2.9100001	3.4100001	9.1999998	76	6000	31	38	6855
32	-1	95	volvo	gas	std	four	sedan	rwd	front	109.1	188.8	68.900002	55.5	2952	ohc	four	141	mpfi	3.78	3.1500001	9.5	114	5400	23	28	16845
13	1	168	toyota	gas	std	two	sedan	rwd	front	94.5	168.7	64	52.599998	2265	dohc	four	98	mpfi	3.24	3.0799999	9.3999996	112	6600	26	29	9298
90	2	164	audi	gas	std	four	sedan	4wd	front	99.400002	176.60001	66.400002	54.299999	2824	ohc	five	136	mpfi	3.1900001	3.4000001	8	115	5500	18	22	17450
63	0	85	honda	gas	std	four	sedan	fwd	front	96.5	175.39999	62.5	54.099998	2372	ohc	four	110	1bbl	3.1500001	3.5799999	9	86	5800	27	33	10295
64	1	158	audi	gas	turbo	four	sedan	fwd	front	105.8	192.7	71.400002	55.900002	3086	ohc	five	131	mpfi	3.1300001	3.4000001	8.3000002	140	5500	17	20	23875
52	-2	103	volvo	gas	turbo	four	sedan	rwd	front	104.3	188.8	67.199997	56.200001	3045	ohc	four	130	mpfi	3.6199999	3.1500001	7.5	162	5100	17	22	18420
97	-1	74	volvo	gas	std	four	wagon	rwd	front	104.3	188.8	67.199997	57.5	3042	ohc	four	141	mpfi	3.78	3.1500001	9.5	114	5400	24	28	16515
46	1	148	dodge	gas	std	four	hatchback	fwd	front	93.699997	157.3	63.799999	50.599998	1967	ohc	four	90	2bbl	2.97	3.23	9.3999996	68	5500	31	38	6229
84	1	118	dodge	gas	std	two	hatchback	fwd	front	93.699997	157.3	63.799999	50.799999	1876	ohc	four	90	2bbl	2.97	3.23	9.4099998	68	5500	37	41	5572
78	1	125	mitsubishi	gas	std	four	sedan	fwd	front	96.300003	172.39999	65.400002	51.599998	2405	ohc	four	122	2bbl	3.3499999	3.46	8.5	88	5000	25	32	8189
40	1	103	nissan	gas	std	four	wagon	fwd	front	94.5	170.2	63.799999	53.5	2037	ohc	four	97	2bbl	3.1500001	3.29	9.3999996	69	5200	31	37	7999
2	1	119	plymouth	gas	turbo	two	hatchback	fwd	front	93.699997	157.3	63.799999	50.799999	2128	ohc	four	98	spdi	3.03	3.3900001	7.5999999	102	5500	24	30	7957
34	2	104	saab	gas	std	four	sedan	fwd	front	99.099998	186.60001	66.5	56.099998	2758	ohc	four	121	mpfi	3.54	3.0699999	9.3000002	110	5250	21	28	15510
60	3	197	toyota	gas	std	two	hatchback	rwd	front	102.9	183.5	67.699997	52	2976	dohc	six	171	mpfi	3.27	3.3499999	9.3000002	161	5200	20	24	16558
105	3	194	nissan	gas	std	two	hatchback	rwd	front	91.300003	170.7	67.900002	49.700001	3071	ohcv	six	181	mpfi	3.4300001	3.27	9	160	5200	19	25	17199
22	0	106	honda	gas	std	two	hatchback	fwd	front	96.5	167.5	65.199997	53.299999	2289	ohc	four	110	1bbl	3.1500001	3.5799999	9	86	5800	27	33	9095
67	0	106	honda	gas	std	two	hatchback	fwd	front	96.5	167.5	65.199997	53.299999	2236	ohc	four	110	1bbl	3.1500001	3.5799999	9	86	5800	27	33	7895
16	0	128	nissan	gas	std	four	sedan	fwd	front	100.4	181.7	66.5	55.099998	3095	ohcv	six	181	mpfi	3.4300001	3.27	9	152	5200	17	22	13499
92	1	148	dodge	gas	std	four	sedan	fwd	front	93.699997	157.3	63.799999	50.599998	1989	ohc	four	90	2bbl	2.97	3.23	9.3999996	68	5500	31	38	7609
54	2	134	toyota	gas	std	two	hardtop	rwd	front	98.400002	176.2	65.599998	52	2540	ohc	four	146	mpfi	3.6199999	3.5	9.3000002	116	4800	24	30	8449
99	0	102	subaru	gas	std	four	sedan	fwd	front	97.199997	172	65.400002	52.5	2340	ohcf	four	108	mpfi	3.6199999	2.6400001	9	94	5200	26	32	9960
48	0	91	toyota	diesel	std	four	hatchback	fwd	front	95.699997	166.3	64.400002	52.799999	2275	ohc	four	110	idi	3.27	3.3499999	22.5	56	4500	38	47	7788
10	0	91	toyota	diesel	std	four	sedan	fwd	front	95.699997	166.3	64.400002	53	2275	ohc	four	110	idi	3.27	3.3499999	22.5	56	4500	34	36	7898
4	1	119	plymouth	gas	std	two	hatchback	fwd	front	93.699997	157.3	63.799999	50.799999	1918	ohc	four	90	2bbl	2.97	3.23	9.3999996	68	5500	37	41	5572
81	1	128	nissan	gas	std	two	sedan	fwd	front	94.5	165.3	63.799999	54.5	1951	ohc	four	97	2bbl	3.1500001	3.29	9.3999996	69	5200	31	37	7299
30	2	94	volkswagen	gas	std	four	sedan	fwd	front	97.300003	171.7	65.5	55.700001	2212	ohc	four	109	mpfi	3.1900001	3.4000001	9	85	5250	27	34	8195
75	-1	93	mercedes-benz	diesel	turbo	four	wagon	rwd	front	110	190.89999	70.300003	58.700001	3750	ohc	five	183	idi	3.5799999	3.6400001	21.5	123	4350	22	25	28248
24	-1	95	volvo	gas	std	four	sedan	rwd	front	109.1	188.8	68.900002	55.5	3012	ohcv	six	173	mpfi	3.5799999	2.8699999	8.8000002	134	5500	18	23	21485
37	3	153	mitsubishi	gas	turbo	two	hatchback	fwd	front	96.300003	173	65.400002	49.400002	2370	ohc	four	110	spdi	3.1700001	3.46	7.5	116	5500	23	30	9959
18	0	93	mercedes-benz	diesel	turbo	two	hardtop	rwd	front	106.7	187.5	70.300003	54.900002	3495	ohc	five	183	idi	3.5799999	3.6400001	21.5	123	4350	22	25	28176
95	1	148	dodge	gas	std	four	sedan	fwd	front	93.699997	157.3	63.799999	50.599998	1989	ohc	four	90	2bbl	2.97	3.23	9.3999996	68	5500	31	38	6692
107	0	110	honda	gas	std	four	sedan	fwd	front	96.5	163.39999	64	54.5	2010	ohc	four	92	1bbl	2.9100001	3.4100001	9.1999998	76	6000	30	34	7295
69	1	103	nissan	gas	std	four	wagon	fwd	front	94.5	170.2	63.799999	53.5	2024	ohc	four	97	2bbl	3.1500001	3.29	9.3999996	69	5200	31	37	7349
57	0	115	mazda	gas	std	four	sedan	fwd	front	98.800003	177.8	66.5	55.5	2410	ohc	four	122	2bbl	3.3900001	3.3900001	8.6000004	84	4800	26	32	10245
102	2	134	toyota	gas	std	two	hardtop	rwd	front	98.400002	176.2	65.599998	52	2536	ohc	four	146	mpfi	3.6199999	3.5	9.3000002	116	4800	24	30	9639
51	1	125	mitsubishi	gas	std	four	sedan	fwd	front	96.300003	172.39999	65.400002	51.599998	2365	ohc	four	122	2bbl	3.3499999	3.46	8.5	88	5000	25	32	6989
96	1	122	nissan	gas	std	four	sedan	fwd	front	94.5	165.3	63.799999	54.5	1938	ohc	four	97	2bbl	3.1500001	3.29	9.3999996	69	5200	31	37	6849
45	1	231	nissan	gas	std	two	hatchback	rwd	front	99.199997	178.5	67.900002	49.700001	3139	ohcv	six	181	mpfi	3.4300001	3.27	9	160	5200	19	25	18399
89	3	194	nissan	gas	turbo	two	hatchback	rwd	front	91.300003	170.7	67.900002	49.700001	3139	ohcv	six	181	mpfi	3.4300001	3.27	7.8000002	200	5200	17	23	19699
83	1	98	chevrolet	gas	std	two	hatchback	fwd	front	94.5	155.89999	63.599998	52	1874	ohc	four	90	2bbl	3.03	3.1099999	9.6000004	70	5400	38	43	6295
7	-1	90	toyota	gas	std	four	sedan	rwd	front	104.5	187.8	66.5	54.099998	3131	dohc	six	171	mpfi	3.27	3.3499999	9.1999998	156	5200	20	24	15690
39	0	106	nissan	gas	std	four	sedan	fwd	front	97.199997	173.39999	65.199997	54.700001	2302	ohc	four	120	2bbl	3.3299999	3.47	8.5	97	5200	27	34	9549
1	0	85	subaru	gas	std	four	wagon	4wd	front	96.900002	173.60001	65.400002	54.900002	2420	ohcf	four	108	2bbl	3.6199999	2.6400001	9	82	4800	23	29	8013
33	1	118	dodge	gas	turbo	two	hatchback	fwd	front	93.699997	157.3	63.799999	50.799999	2128	ohc	four	98	mpfi	3.03	3.3900001	7.5999999	102	5500	24	30	7957
27	3	142	mercedes-benz	gas	std	two	convertible	rwd	front	96.599998	180.3	70.5	50.799999	3685	ohcv	eight	234	mpfi	3.46	3.0999999	8.3000002	155	4750	16	18	35056
72	0	81	toyota	gas	std	four	wagon	4wd	front	95.699997	169.7	63.599998	59.099998	2290	ohc	four	92	2bbl	3.05	3.03	9	62	4800	27	32	7898
21	-1	65	toyota	gas	std	four	hatchback	fwd	front	102.4	175.60001	66.5	53.900002	2458	ohc	four	122	mpfi	3.3099999	3.54	8.6999998	92	4200	27	32	11248
66	0	91	toyota	gas	std	four	hatchback	fwd	front	95.699997	166.3	64.400002	52.799999	2109	ohc	four	98	2bbl	3.1900001	3.03	9	70	4800	30	37	7198
15	1	128	nissan	gas	std	two	hatchback	fwd	front	94.5	165.60001	63.799999	53.299999	2028	ohc	four	97	2bbl	3.1500001	3.29	9.3999996	69	5200	31	37	7799
59	-1	93	mercedes-benz	diesel	turbo	four	sedan	rwd	front	115.6	202.60001	71.699997	56.299999	3770	ohc	five	183	idi	3.5799999	3.6400001	21.5	123	4350	22	25	31600
104	3	153	mitsubishi	gas	std	two	hatchback	fwd	front	96.300003	173	65.400002	49.400002	2328	ohc	four	122	2bbl	3.3499999	3.46	8.5	88	5000	25	32	8499
53	-2	103	volvo	gas	std	four	sedan	rwd	front	104.3	188.8	67.199997	56.200001	2935	ohc	four	141	mpfi	3.78	3.1500001	9.5	114	5400	24	28	15985
98	2	83	subaru	gas	std	two	hatchback	fwd	front	93.699997	156.89999	63.400002	53.700001	2050	ohcf	four	97	2bbl	3.6199999	2.3599999	9	69	4900	31	36	5118
9	3	197	toyota	gas	std	two	hatchback	rwd	front	102.9	183.5	67.699997	52	3016	dohc	six	171	mpfi	3.27	3.3499999	9.3000002	161	5200	19	24	15998
86	1	161	mitsubishi	gas	turbo	two	hatchback	fwd	front	93	157.3	63.799999	50.799999	2145	ohc	four	98	spdi	3.03	3.3900001	7.5999999	102	5500	24	30	7689
3	1	113	mazda	gas	std	four	sedan	fwd	front	93.099998	166.8	64.199997	54.099998	1945	ohc	four	91	2bbl	3.03	3.1500001	9	68	5000	31	38	6695
80	1	107	honda	gas	std	two	sedan	fwd	front	96.5	169.10001	66	51	2293	ohc	four	110	2bbl	3.1500001	3.5799999	9.1000004	100	5500	25	31	10345
29	-1	65	toyota	gas	std	four	sedan	fwd	front	102.4	175.60001	66.5	54.900002	2414	ohc	four	122	mpfi	3.3099999	3.54	8.6999998	92	4200	27	32	10898
42	-1	74	volvo	gas	std	four	wagon	rwd	front	104.3	188.8	67.199997	57.5	3034	ohc	four	141	mpfi	3.78	3.1500001	9.5	114	5400	23	28	13415
23	0	89	subaru	gas	std	four	wagon	fwd	front	97	173.5	65.400002	53	2290	ohcf	four	108	2bbl	3.6199999	2.6400001	9	82	4800	28	32	7463
36	0	91	toyota	gas	std	four	sedan	fwd	front	95.699997	166.3	64.400002	52.799999	2140	ohc	four	98	2bbl	3.1900001	3.03	9	70	4800	28	34	9258
74	2	94	volkswagen	gas	std	four	sedan	fwd	front	97.300003	171.7	65.5	55.700001	2300	ohc	four	109	mpfi	3.1900001	3.4000001	10	100	5500	26	32	9995
68	2	94	volkswagen	diesel	std	four	sedan	fwd	front	97.300003	171.7	65.5	55.700001	2264	ohc	four	97	idi	3.01	3.4000001	23	52	4800	37	46	7995
62	1	158	audi	gas	std	four	sedan	fwd	front	105.8	192.7	71.400002	55.700001	2844	ohc	five	136	mpfi	3.1900001	3.4000001	8.5	110	5500	19	25	17710
94	0	91	toyota	gas	std	four	hatchback	fwd	front	95.699997	166.3	64.400002	52.799999	2122	ohc	four	98	2bbl	3.1900001	3.03	9	70	4800	28	34	8358
56	-1	65	toyota	diesel	turbo	four	sedan	fwd	front	102.4	175.60001	66.5	54.900002	2480	ohc	four	110	idi	3.27	3.3499999	22.5	73	4500	30	33	10698
101	2	104	saab	gas	std	four	sedan	fwd	front	99.099998	186.60001	66.5	56.099998	2695	ohc	four	121	mpfi	3.54	3.0699999	9.3000002	110	5250	21	28	12170
50	0	102	subaru	gas	turbo	four	sedan	4wd	front	97	172	65.400002	54.299999	2510	ohcf	four	108	mpfi	3.6199999	2.6400001	7.6999998	111	4800	24	29	11259
88	1	87	toyota	gas	std	two	hatchback	fwd	front	95.699997	158.7	63.599998	54.5	2040	ohc	four	92	2bbl	3.05	3.03	9	62	4800	31	38	6338
12	2	122	volkswagen	gas	std	two	sedan	fwd	front	97.300003	171.7	65.5	55.700001	2209	ohc	four	109	mpfi	3.1900001	3.4000001	9	85	5250	27	34	7975
44	3	150	saab	gas	std	two	hatchback	fwd	front	99.099998	186.60001	66.5	56.099998	2658	ohc	four	121	mpfi	3.54	3.0699999	9.3100004	110	5250	21	28	11850
6	0	161	peugot	diesel	turbo	four	sedan	rwd	front	107.9	186.7	68.400002	56.700001	3252	l	four	152	idi	3.7	3.52	21	95	4150	28	33	17950
38	2	161	mitsubishi	gas	std	two	hatchback	fwd	front	93.699997	157.3	64.400002	50.799999	1944	ohc	four	92	2bbl	2.97	3.23	9.3999996	68	5500	31	38	6189
77	2	122	volkswagen	diesel	std	two	sedan	fwd	front	97.300003	171.7	65.5	55.700001	2261	ohc	four	97	idi	3.01	3.4000001	23	52	4800	37	46	7775
26	1	168	toyota	gas	std	two	hatchback	rwd	front	94.5	168.7	64	52.599998	2204	ohc	four	98	2bbl	3.1900001	3.03	9	70	4800	29	34	8238
71	-1	65	toyota	gas	std	four	hatchback	fwd	front	102.4	175.60001	66.5	53.900002	2414	ohc	four	122	mpfi	3.3099999	3.54	8.6999998	92	4200	27	32	9988
20	0	91	toyota	gas	std	four	sedan	fwd	front	95.699997	166.3	64.400002	53	2081	ohc	four	98	2bbl	3.1900001	3.03	9	70	4800	30	37	6938
65	1	129	mazda	gas	std	two	hatchback	fwd	front	98.800003	177.8	66.5	53.700001	2385	ohc	four	122	2bbl	3.3900001	3.3900001	8.6000004	84	4800	26	32	8845
14	1	128	nissan	gas	std	two	sedan	fwd	front	94.5	165.3	63.799999	54.5	1889	ohc	four	97	2bbl	3.1500001	3.29	9.3999996	69	5200	31	37	5499
91	1	154	plymouth	gas	std	four	sedan	fwd	front	93.699997	167.3	63.799999	50.799999	1989	ohc	four	90	2bbl	2.97	3.23	9.3999996	68	5500	31	38	6692
8	0	78	honda	gas	std	four	wagon	fwd	front	96.5	157.10001	63.900002	58.299999	2024	ohc	four	92	1bbl	2.9200001	3.4100001	9.1999998	76	6000	30	34	7295
85	1	128	nissan	gas	std	two	sedan	fwd	front	94.5	165.3	63.799999	54.5	1918	ohc	four	97	2bbl	3.1500001	3.29	9.3999996	69	5200	31	37	6649
58	-1	95	volvo	gas	turbo	four	sedan	rwd	front	109.1	188.8	68.900002	55.5	3062	ohc	four	141	mpfi	3.78	3.1500001	9.5	114	5400	19	25	22625
103	0	161	peugot	gas	turbo	four	sedan	rwd	front	108	186.7	68.300003	56	3130	l	four	134	mpfi	3.6099999	3.21	7	142	5600	18	24	18150
47	1	101	honda	gas	std	two	hatchback	fwd	front	93.699997	150	64	52.599998	1956	ohc	four	92	1bbl	2.9100001	3.4100001	9.1999998	76	6000	30	34	7129
28	3	150	saab	gas	turbo	two	hatchback	fwd	front	99.099998	186.60001	66.5	56.099998	2808	dohc	four	121	mpfi	3.54	3.0699999	9	160	5500	19	26	18150
41	2	161	mitsubishi	gas	std	two	hatchback	fwd	front	93.699997	157.3	64.400002	50.799999	2004	ohc	four	92	2bbl	2.97	3.23	9.3999996	68	5500	31	38	6669
79	1	74	toyota	gas	std	four	hatchback	fwd	front	95.699997	158.7	63.599998	54.5	2015	ohc	four	92	2bbl	3.05	3.03	9	62	4800	31	38	6488
73	2	168	nissan	gas	std	two	hardtop	fwd	front	95.099998	162.39999	63.799999	53.299999	2008	ohc	four	97	2bbl	3.1500001	3.29	9.3999996	69	5200	31	37	8249
35	1	104	mazda	gas	std	two	hatchback	fwd	front	93.099998	159.10001	64.199997	54.099998	1905	ohc	four	91	2bbl	3.03	3.1500001	9	68	5000	31	38	6795
61	2	121	chevrolet	gas	std	two	hatchback	fwd	front	88.400002	141.10001	60.299999	53.200001	1488	l	three	61	2bbl	2.9100001	3.03	9.5	48	5100	47	53	5151
106	0	77	toyota	gas	std	four	wagon	fwd	front	95.699997	169.7	63.599998	59.099998	2280	ohc	four	92	2bbl	3.05	3.03	9	62	4800	31	37	6918
55	1	87	toyota	gas	std	two	hatchback	fwd	front	95.699997	158.7	63.599998	54.5	1985	ohc	four	92	2bbl	3.05	3.03	9	62	4800	35	39	5348
100	0	102	subaru	gas	std	four	sedan	fwd	front	97.199997	172	65.400002	52.5	2190	ohcf	four	108	2bbl	3.6199999	2.6400001	9.5	82	4400	28	33	7775
17	3	145	dodge	gas	turbo	two	hatchback	fwd	front	95.900002	173.2	66.300003	50.200001	2811	ohc	four	156	mfi	3.5999999	3.9000001	7	145	5000	19	24	12964
93	1	104	mazda	gas	std	two	hatchback	fwd	front	93.099998	159.10001	64.199997	54.099998	1900	ohc	four	91	2bbl	3.03	3.1500001	9	68	5000	31	38	6095
87	1	129	mazda	gas	std	two	hatchback	fwd	front	98.800003	177.8	66.5	53.700001	2385	ohc	four	122	2bbl	3.3900001	3.3900001	8.6000004	84	4800	26	32	10595
49	1	154	plymouth	gas	std	four	hatchback	fwd	front	93.699997	157.3	63.799999	50.599998	1967	ohc	four	90	2bbl	2.97	3.23	9.3999996	68	5500	31	38	6229
11	-1	95	volvo	diesel	turbo	four	sedan	rwd	front	109.1	188.8	68.900002	55.5	3217	ohc	six	145	idi	3.01	3.4000001	23	106	4800	26	27	22470
43	0	115	mazda	gas	std	four	sedan	fwd	front	98.800003	177.8	66.5	55.5	2410	ohc	four	122	2bbl	3.3900001	3.3900001	8.6000004	84	4800	26	32	8495
5	-1	74	volvo	gas	turbo	four	wagon	rwd	front	104.3	188.8	67.199997	57.5	3157	ohc	four	130	mpfi	3.6199999	3.1500001	7.5	162	5100	17	22	18950
82	0	91	toyota	gas	std	four	sedan	fwd	front	95.699997	166.3	64.400002	53	2094	ohc	four	98	2bbl	3.1900001	3.03	9	70	4800	38	47	7738
\.


--
-- Greenplum Database database dump complete
--

