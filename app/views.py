from flask import render_template
from app import app
import pymysql as mdb
from flask.json import jsonify
import pandas as pd
#from scipy import stats

import math
from flask import Flask, render_template, flash, redirect, url_for, jsonify
from app import app
from flask import request
#import MySQLdb
import sys
import numpy
import json
#import scipy.stats
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import scipy as sp
import json as js
import urllib
#import MySQLdb as sql
#import sklearn as skl
import calendar
import time
import os
import sys
#from scipy import stats
import datetime


db = mdb.connect(user="root", host="localhost", db="CityBikes", charset='utf8')

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")
        
@app.route('/home')
def home():
	return render_template("home.html")


@app.route('/slideshow')
def slideshow():
	return render_template("slideshow.html"),
        

	
@app.route("/planner")
def planner():
        print request.args.get('startStation', '')

	print("inside planner")

	startStation_input = request.args.get('startStation', '')
	startStation_input = startStation_input.lstrip().rstrip()

        endStation_input = request.args.get('endStation', '')
	endStation_input = endStation_input.lstrip().rstrip()

	#hour_input = request.args.get('hour', '')
	#hour_input = hour_input.lstrip().rstrip()

        #minute_input = request.args.get('minute', '')
	#minute_input = minute_input.lstrip().rstrip()

        time_input = request.args.get('time', '')
	time_input = time_input.lstrip().rstrip()
	
	date_input = request.args.get('date', '')
	date = date_input.lstrip().rstrip().split("-")
	year_input = date[0];month_input = date[1];day_input = date[2];

	departuretime_input = request.args.get('departuretime', '')
	departuretime = departuretime_input.lstrip().rstrip().split(":")
	hour_input = departuretime[0];minute_input = departuretime[1]


	#######################################################################################################################################
	#### initializing parameters

	locations =  [['Station 72, W 52 St & 11 Ave',40.76727216,-73.99392888,39,72],['Station 79, Franklin St & W Broadway',40.71911552,-74.00666661,33,79],['Station 82, St James Pl & Pearl St',40.71117416,-74.00016545,27,82],['Station 83, Atlantic Ave & Fort Greene Pl',40.68382604,-73.97632328,61,83],['Station 116, W 17 St & 8 Ave',40.74177603,-74.00149746,39,116],['Station 119, Park Ave & St Edwards St',40.69608941,-73.97803415,19,119],['Station 120, Lexington Ave & Classon Ave',40.68676793,-73.95928168,19,120],['Station 127, Barrow St & Hudson St',40.73172428,-74.00674436,31,127],['Station 128, MacDougal St & Prince St',40.72710258,-74.00297088,29,128],['Station 137, E 56 St & Madison Ave',40.761628,-73.972924,46,137],['Station 143, Clinton St & Joralemon St',40.69239502,-73.99337909,24,143],['Station 144, Nassau St & Navy St',40.69839895,-73.98068914,19,144],['Station 146, Hudson St & Reade St',40.71625008,-74.0091059,39,146],['Station 147, Greenwich St & Warren St',40.71542197,-74.01121978,33,147],['Station 150, E 2 St & Avenue C',40.7208736,-73.98085795,31,150],['Station 151, Cleveland Pl & Spring St',40.7218158,-73.99720307,33,151],['Station 152, Warren St & Church St',40.71473993,-74.00910627,29,152],['Station 153, E 40 St & 5 Ave',40.752062307,-73.9816324043,55,153],['Station 157, Henry St & Atlantic Ave',40.69089272,-73.99612349,23,157],['Station 160, E 37 St & Lexington Ave',40.748238,-73.978311,26,160],['Station 161, LaGuardia Pl & W 3 St',40.72917025,-73.99810231,35,161],['Station 164, E 47 St & 2 Ave',40.75323098,-73.97032517,47,164],['Station 167, E 39 St & 3 Ave',40.7489006,-73.97604882,45,167],['Station 168, W 18 St & 6 Ave',40.73971301,-73.99456405,47,168],['Station 173, Broadway & W 49 St',40.76064679,-73.98442659,51,173],['Station 174, E 25 St & 1 Ave',40.7381765,-73.97738662,30,174],['Station 195, Liberty St & Broadway',40.70905623,-74.01043382,45,195],['Station 212, W 16 St & The High Line',40.74334935,-74.00681753,28,212],['Station 216, Columbia Heights & Cranberry St',40.70037867,-73.99548059,20,216],['Station 217, Old Fulton St',40.70277159,-73.99383605,39,217],['Station 218, Gallatin Pl & Livingston St',40.69028437,-73.98707105,38,218],['Station 223, W 13 St & 7 Ave',40.73781509,-73.99994661,33,223],['Station 224, Spruce St & Nassau St',40.71146364,-74.00552427,31,224],['Station 225, W 14 St & The High Line',40.74195138,-74.00803013,37,225],['Station 228, E 48 St & 3 Ave',40.7546011026,-73.971878855,55,228],['Station 229, Great Jones St',40.72743423,-73.99379025,22,229],['Station 232, Cadman Plaza E & Tillary St',40.69597683,-73.99014892,23,232],['Station 233, Joralemon St & Adams St',40.69246277,-73.98963911,39,233],['Station 236, St Marks Pl & 2 Ave',40.7284186,-73.98713956,39,236],['Station 237, E 11 St & 2 Ave',40.73047309,-73.98672378,39,237],['Station 238, Bank St & Washington St',40.7361967,-74.00859207,31,238],['Station 239, Willoughby St & Fleet St',40.69196566,-73.9813018,31,239],['Station 241, DeKalb Ave & S Portland Ave',40.68981035,-73.97493121,23,241],['Station 242, Flushing Ave & Carlton Ave',40.69788349,-73.97350332,23,242],['Station 243, Fulton St & Rockwell Pl',40.688226,-73.979382,31,243],['Station 244, Willoughby Ave & Hall St',40.69196035,-73.96536851,31,244],['Station 245, Myrtle Ave & St Edwards St',40.69327018,-73.97703874,23,245],['Station 247, Perry St & Bleecker St',40.73535398,-74.00483091,20,247],['Station 248, Laight St & Hudson St',40.72185379,-74.00771779,23,248],['Station 249, Harrison St & Hudson St',40.71870987,-74.0090009,27,249],['Station 250, Lafayette St & Jersey St',40.72456089,-73.99565293,39,250],['Station 251, Mott St & Prince St',40.72317958,-73.99480012,27,251],['Station 252, MacDougal St & Washington Sq',40.73226398,-73.99852205,33,252],['Station 253, W 13 St & 5 Ave',40.73543934,-73.99453948,3,253],['Station 254, W 11 St & 6 Ave',40.73532427,-73.99800419,3,254],['Station 257, Lispenard St & Broadway',40.71939226,-74.00247214,38,257],['Station 258, DeKalb Ave & Vanderbilt Ave',40.68940747,-73.96885458,23,258],['Station 259, South St & Whitehall St',40.70122128,-74.01234218,39,259],['Station 260, Broad St & Bridge St',40.70365182,-74.01167797,35,260],['Station 261, Johnson St & Gold St',40.69474881,-73.98362464,27,261],['Station 262, Washington Park',40.69178232,-73.97372989,23,262],['Station 263, Elizabeth St & Hester St',40.71729,-73.996375,31,263],['Station 264, Maiden Ln & Pearl St',40.70706456,-74.00731853,27,264],['Station 265, Stanton St & Chrystie St',40.72229346,-73.99147535,35,265],['Station 266, Avenue D & E 8 St',40.72368361,-73.97574813,24,266],['Station 267, Broadway & W 36 St',40.75097711,-73.98765428,57,267],['Station 268, Howard St & Centre St',40.71910537,-73.99973337,27,268],['Station 270, Adelphi St & Myrtle Ave',40.69308257,-73.97178913,23,270],['Station 271, Ashland Pl & Hanson Pl',40.68528172,-73.97805813,39,271],['Station 274, Lafayette Ave & Fort Greene Pl',40.68691865,-73.976682,31,274],['Station 275, Washington Ave & Greene Ave',40.68650065,-73.96563307,19,275],['Station 276, Duane St & Greenwich St',40.71748752,-74.0104554,25,276],['Station 278, Concord St & Bridge St',40.69766564,-73.98476437,19,278],['Station 279, Peck Slip & Front Street',40.707873,-74.00167,36,279],['Station 280, E 10 St & 5 Ave',40.73331967,-73.99510132,31,280],['Station 281, Grand Army Plaza & Central Park S',40.7643971,-73.97371465,59,281],['Station 282, Kent Ave & S 11 St',40.70827295,-73.96834101,27,282],['Station 284, Greenwich Ave & 8 Ave',40.7390169121,-74.0026376103,43,284],['Station 285, Broadway & E 14 St',40.73454567,-73.99074142,47,285],['Station 289, Monroe St & Classon Ave',40.6845683,-73.95881081,19,289],['Station 290, 2 Ave & E 58 St',40.76020258,-73.96478473,29,290],['Station 291, Madison St & Montgomery St',40.713126,-73.984844,20,291],['Station 293, Lafayette St & E 8 St',40.73028666,-73.9907647,54,293],['Station 294, Washington Square E',40.73049393,-73.9957214,31,294],['Station 295, Pike St & E Broadway',40.71406667,-73.99293911,24,295],['Station 296, Division St & Bowery',40.71413089,-73.9970468,34,296],['Station 297, E 15 St & 3 Ave',40.734232,-73.986923,27,297],['Station 298, 3 Ave & Schermerhorn St',40.68683208,-73.9796772,35,298],['Station 300, Shevchenko Pl & E 7 St',40.728145,-73.990214,54,300],['Station 301, E 2 St & Avenue B',40.72217444,-73.98368779,16,301],['Station 302, Avenue D & E 3 St',40.72082834,-73.97793172,23,302],['Station 303, Mercer St & Spring St',40.72362738,-73.99949601,31,303],['Station 304, Broadway & Battery Pl',40.70463334,-74.01361706,36,304],['Station 305, E 58 St & 3 Ave',40.76095756,-73.96724467,33,305],['Station 306, Cliff St & Fulton St',40.70823502,-74.00530063,37,306],['Station 307, Canal St & Rutgers St',40.71427487,-73.98990025,31,307],['Station 308, St James Pl & Oliver St',40.71307916,-73.99851193,27,308],['Station 309, Murray St & West St',40.7149787,-74.013012,41,309],['Station 310, State St & Smith St',40.68926942,-73.98912867,36,310],['Station 311, Norfolk St & Broome St',40.7172274,-73.98802084,30,311],['Station 312, Allen St & E Houston St',40.722055,-73.989111,31,312],['Station 313, Washington Ave & Park Ave',40.69610226,-73.96751037,23,313],['Station 314, Cadman Plaza West & Montague St',40.69383,-73.990539,39,314],['Station 315, South St & Gouverneur Ln',40.70355377,-74.00670227,29,315],['Station 316, Fulton St & William St',40.70955958,-74.00653609,43,316],['Station 317, E 6 St & Avenue B',40.72453734,-73.98185424,27,317],['Station 318, E 43 St & Vanderbilt Ave',40.75320159,-73.9779874,31,318],['Station 319, Park Pl & Church St',40.71336124,-74.00937622,35,319],['Station 320, Leonard St & Church St',40.717571,-74.005549,39,320],['Station 321, Cadman Plaza E & Red Cross Pl',40.69991755,-73.98971773,27,321],['Station 322, Clinton St & Tillary St',40.696192,-73.991218,31,322],['Station 323, Lawrence St & Willoughby St',40.69236178,-73.98631746,39,323],['Station 324, DeKalb Ave & Hudson Ave',40.689888,-73.981013,51,324],['Station 325, E 19 St & 3 Ave',40.73624527,-73.98473765,35,325],['Station 326, E 11 St & 1 Ave',40.72953837,-73.98426726,27,326],['Station 327, Vesey Pl & River Terrace',40.7153379,-74.01658354,39,327],['Station 328, Watts St & Greenwich St',40.72405549,-74.00965965,23,328],['Station 329, Greenwich St & N Moore St',40.72043411,-74.01020609,31,329],['Station 330, Reade St & Broadway',40.71450451,-74.00562789,39,330],['Station 331, Pike St & Monroe St',40.71173107,-73.99193043,27,331],['Station 332, Cherry St',40.71219906,-73.97948148,24,332],['Station 334, W 20 St & 7 Ave',40.74238787,-73.99726235,31,334],['Station 335, Washington Pl & Broadway',40.72903917,-73.99404649,27,335],['Station 336, Sullivan St & Washington Sq',40.73047747,-73.99906065,36,336],['Station 337, Old Slip & Front St',40.7037992,-74.00838676,37,337],['Station 339, Avenue D & E 12 St',40.72580614,-73.97422494,24,339],['Station 340, Madison St & Clinton St',40.71269042,-73.98776323,27,340],['Station 341, Stanton St & Mangin St',40.71782143,-73.97628939,19,341],['Station 342, Columbia St & Rivington St',40.71739973,-73.98016555,29,342],['Station 343, Clinton Ave & Flushing Ave',40.69794,-73.96986848,23,343],['Station 344, Monroe St & Bedford Ave',40.6851443,-73.95380904,23,344],['Station 345, W 13 St & 6 Ave',40.73649403,-73.99704374,35,345],['Station 346, Bank St & Hudson St',40.73652889,-74.00618026,27,346],['Station 347, W Houston St & Hudson St',40.72873888,-74.00748842,35,347],['Station 348, W Broadway & Spring St',40.72490985,-74.00154702,42,348],['Station 349, Rivington St & Ridge St',40.71850211,-73.98329859,23,349],['Station 350, Clinton St & Grand St',40.71559509,-73.9870295,27,350],['Station 351, Front St & Maiden Ln',40.70530954,-74.00612572,39,351],['Station 352, W 56 St & 6 Ave',40.76340613,-73.97722479,36,352],['Station 353, S Portland Ave & Hanson Pl',40.68539567,-73.97431458,27,353],['Station 354, Emerson Pl & Myrtle Ave',40.69363137,-73.96223558,31,354],['Station 355, Bayard St & Baxter St',40.71602118,-73.99974372,43,355],['Station 356, Bialystoker Pl & Delancey St',40.71622644,-73.98261206,23,356],['Station 357, E 11 St & Broadway',40.73261787,-73.99158043,27,357],['Station 358, Christopher St & Greenwich St',40.73291553,-74.00711384,36,358],['Station 359, E 47 St & Park Ave',40.75510267,-73.97498696,55,359],['Station 360, William St & Pine St',40.70717936,-74.00887308,39,360],['Station 361, Allen St & Hester St',40.71605866,-73.99190759,43,361],['Station 362, Broadway & W 37 St',40.75172632,-73.98753523,57,362],['Station 363, West Thames St',40.70834698,-74.01713445,48,363],['Station 364, Lafayette Ave & Classon Ave',40.68900443,-73.96023854,27,364],['Station 365, Fulton St & Grand Ave',40.68223166,-73.9614583,31,365],['Station 366, Clinton Ave & Myrtle Ave',40.693261,-73.968896,33,366],['Station 367, E 53 St & Lexington Ave',40.75828065,-73.97069431,34,367],['Station 368, Carmine St & 6 Ave',40.73038599,-74.00214988,39,368],['Station 369, Washington Pl & 6 Ave',40.73224119,-74.00026394,35,369],['Station 372, Franklin Ave & Myrtle Ave',40.694528,-73.958089,27,372],['Station 373, Willoughby Ave & Walworth St',40.69331716,-73.95381995,19,373],['Station 375, Mercer St & Bleecker St',40.72679454,-73.99695094,30,375],['Station 376, John St & William St',40.70862144,-74.00722156,43,376],['Station 377, 6 Ave & Canal St',40.72243797,-74.00566443,47,377],['Station 379, W 31 St & 7 Ave',40.749156,-73.9916,42,379],['Station 380, W 4 St & 7 Ave S',40.73401143,-74.00293877,39,380],['Station 382, University Pl & E 14 St',40.73492695,-73.99200509,36,382],['Station 383, Greenwich Ave & Charles St',40.735238,-74.000271,39,383],['Station 384, Fulton St & Waverly Ave',40.68317813,-73.9659641,31,384],['Station 385, E 55 St & 2 Ave',40.75797322,-73.96603308,28,385],['Station 386, Centre St & Worth St',40.71494807,-74.00234482,43,386],['Station 387, Centre St & Chambers St',40.71273266,-74.0046073,39,387],['Station 388, W 26 St & 10 Ave',40.749717753,-74.002950346,35,388],['Station 389, Broadway & Berry St',40.71044554,-73.96525063,27,389],['Station 390, Duffield St & Willoughby St',40.69221589,-73.9842844,31,390],['Station 391, Clark St & Henry St',40.69760127,-73.99344559,31,391],['Station 392, Jay St & Tech Pl',40.695065,-73.987167,32,392],['Station 393, E 5 St & Avenue C',40.72299208,-73.97995466,31,393],['Station 394, E 9 St & Avenue C',40.72521311,-73.97768752,32,394],['Station 395, Bond St & Schermerhorn St',40.68807003,-73.98410637,30,395],['Station 396, Lefferts Pl & Franklin Ave',40.680342423,-73.9557689392,25,396],['Station 397, Fulton St & Clermont Ave',40.68415748,-73.96922273,27,397],['Station 398, Atlantic Ave & Furman St',40.69165183,-73.9999786,31,398],['Station 399, Lafayette Ave & St James Pl',40.68851534,-73.9647628,27,399],['Station 400, Pitt St & Stanton St',40.71926081,-73.98178024,15,400],['Station 401, Allen St & Rivington St',40.72019576,-73.98997825,40,401],['Station 402, Broadway & E 22 St',40.7403432,-73.98955109,42,402],['Station 403, E 2 St & 2 Ave',40.72502876,-73.99069656,31,403],['Station 404, 9 Ave & W 14 St',40.7405826,-74.00550867,39,404],['Station 405, Washington St & Gansevoort St',40.739323,-74.008119,40,405],['Station 406, Hicks St & Montague St',40.69512845,-73.99595065,34,406],['Station 407, Henry St & Poplar St',40.700469,-73.991454,43,407],['Station 408, Market St & Cherry St',40.71076228,-73.99400398,23,408],['Station 409, DeKalb Ave & Skillman St',40.6906495,-73.95643107,19,409],['Station 410, Suffolk St & Stanton St',40.72066442,-73.98517977,35,410],['Station 411, E 6 St & Avenue D',40.72228087,-73.97668709,23,411],['Station 412, Forsyth St & Canal St',40.7158155,-73.99422366,20,412],['Station 414, Pearl St & Anchorage Pl',40.70281858,-73.98765762,24,414],['Station 415, Pearl St & Hanover Square',40.7047177,-74.00926027,42,415],['Station 416, Cumberland St & Lafayette Ave',40.68753406,-73.97265183,31,416],['Station 417, Barclay St & Church St',40.71291224,-74.01020234,47,417],['Station 418, Front St & Gold St',40.70224,-73.982578,23,418],['Station 419, Carlton Ave & Park Ave',40.69580705,-73.97355569,23,419],['Station 420, Clermont Ave & Lafayette Ave',40.68764484,-73.96968902,23,420],['Station 421, Clermont Ave & Park Ave',40.69573398,-73.97129668,19,421],['Station 422, W 59 St & 10 Ave',40.770513,-73.988038,55,422],['Station 423, W 54 St & 9 Ave',40.76584941,-73.98690506,39,423],['Station 426, West St & Chambers St',40.71754834,-74.01322069,31,426],['Station 427, Bus Slip & State St',40.701907,-74.013942,47,427],['Station 428, E 3 St & 1 Ave',40.72467721,-73.98783413,31,428],['Station 430, York St & Jay St',40.7014851,-73.98656928,27,430],['Station 431, Hanover Pl & Livingston St',40.68864636,-73.98263429,30,431],['Station 432, E 7 St & Avenue A',40.72621788,-73.98379855,31,432],['Station 433, E 13 St & Avenue A',40.72955361,-73.98057249,39,433],['Station 434, 9 Ave & W 18 St',40.74317449,-74.00366443,27,434],['Station 435, W 21 St & 6 Ave',40.74173969,-73.99415556,47,435],['Station 436, Hancock St & Bedford Ave',40.68216564,-73.95399026,27,436],['Station 437, Macon St & Nostrand Ave',40.6809833854,-73.9500479759,27,437],['Station 438, St Marks Pl & 1 Ave',40.72779126,-73.98564945,27,438],['Station 439, E 4 St & 2 Ave',40.7262807,-73.98978041,39,439],['Station 440, E 45 St & 3 Ave',40.75255434,-73.97282625,29,440],['Station 441, E 52 St & 2 Ave',40.756014,-73.967416,35,441],['Station 442, W 27 St & 7 Ave',40.746647,-73.993915,51,442],['Station 443, Bedford Ave & S 9th St',40.70853074,-73.96408963,23,443],['Station 444, Broadway & W 24 St',40.7423543,-73.98915076,35,444],['Station 445, E 10 St & Avenue A',40.72740794,-73.98142006,42,445],['Station 446, W 24 St & 7 Ave',40.74487634,-73.99529885,39,446],['Station 447, 8 Ave & W 52 St',40.76370739,-73.9851615,31,447],['Station 448, W 37 St & 10 Ave',40.75660359,-73.9979009,31,448],['Station 449, W 52 St & 9 Ave',40.76461837,-73.98789473,31,449],['Station 450, W 49 St & 8 Ave',40.76227205,-73.98788205,59,450],['Station 453, W 22 St & 8 Ave',40.74475148,-73.99915362,38,453],['Station 454, E 51 St & 1 Ave',40.75455731,-73.96592976,35,454],['Station 455, 1 Ave & E 44 St',40.75001986,-73.96905301,39,455],['Station 456, E 53 St & Madison Ave',40.7597108,-73.97402311,35,456],['Station 457, Broadway & W 58 St',40.76695317,-73.98169333,56,457],['Station 458, 11 Ave & W 27 St',40.751396,-74.005226,30,458],['Station 459, W 20 St & 11 Ave',40.746745,-74.007756,49,459],['Station 460, S 4 St & Wythe Ave',40.71285887,-73.96590294,23,460],['Station 461, E 20 St & 2 Ave',40.73587678,-73.98205027,39,461],['Station 462, W 22 St & 10 Ave',40.74691959,-74.00451887,47,462],['Station 463, 9 Ave & W 16 St',40.74206539,-74.00443172,25,463],['Station 464, E 56 St & 3 Ave',40.75934501,-73.96759673,59,464],['Station 465, Broadway & W 41 St',40.75513557,-73.98658032,39,465],['Station 466, W 25 St & 6 Ave',40.74395411,-73.99144871,35,466],['Station 467, Dean St & 4 Ave',40.68312489,-73.97895137,34,467],['Station 468, Broadway & W 55 St',40.7652654,-73.98192338,59,468],['Station 469, Broadway & W 53 St',40.76344058,-73.98268129,51,469],['Station 470, W 20 St & 8 Ave',40.74345335,-74.00004031,37,470],['Station 471, Grand St & Havemeyer St',40.71286844,-73.95698119,31,471],['Station 472, E 32 St & Park Ave',40.7457121,-73.98194829,38,472],['Station 473, Rivington St & Chrystie St',40.72110063,-73.9919254,39,473],['Station 474, 5 Ave & E 29 St',40.7451677,-73.98683077,47,474],['Station 475, E 16 St & Irving Pl',40.73524276,-73.98758561,34,475],['Station 476, E 31 St & 3 Ave',40.74394314,-73.97966069,46,476],['Station 477, W 41 St & 8 Ave',40.75640548,-73.9900262,59,477],['Station 478, 11 Ave & W 41 St',40.76030096,-73.99884222,31,478],['Station 479, 9 Ave & W 45 St',40.76019252,-73.9912551,31,479],['Station 480, W 53 St & 10 Ave',40.76669671,-73.99061728,27,480],['Station 481, S 3 St & Bedford Ave',40.71260486,-73.96264403,25,481],['Station 482, W 15 St & 7 Ave',40.73935542,-73.99931783,39,482],['Station 483, E 12 St & 3 Ave',40.73223272,-73.98889957,35,483],['Station 484, W 44 St & 5 Ave',40.75500254,-73.98014437,44,484],['Station 485, W 37 St & 5 Ave',40.75038009,-73.98338988,39,485],['Station 486, Broadway & W 29 St',40.7462009,-73.98855723,39,486],['Station 487, E 20 St & FDR Drive',40.73314259,-73.97573881,36,487],['Station 488, W 39 St & 9 Ave',40.75645824,-73.99372222,41,488],['Station 489, 10 Ave & W 28 St',40.75066386,-74.00176802,37,489],['Station 490, 8 Ave & W 33 St',40.751551,-73.993934,59,490],['Station 491, E 24 St & Park Ave S',40.74096374,-73.98602213,49,491],['Station 492, W 33 St & 7 Ave',40.75019995,-73.99093085,49,492],['Station 493, W 45 St & 6 Ave',40.7568001,-73.98291153,34,493],['Station 494, W 26 St & 8 Ave',40.74734825,-73.99723551,35,494],['Station 495, W 47 St & 10 Ave',40.76269882,-73.99301222,25,495],['Station 496, E 16 St & 5 Ave',40.73726186,-73.99238967,47,496],['Station 497, E 17 St & Broadway',40.73704984,-73.99009296,59,497],['Station 498, Broadway & W 32 St',40.74854862,-73.98808416,30,498],['Station 499, Broadway & W 60 St',40.76915505,-73.98191841,36,499],['Station 500, Broadway & W 51 St',40.76228826,-73.98336183,48,500],['Station 501, FDR Drive & E 35 St',40.744219,-73.97121214,43,501],['Station 502, Henry St & Grand St',40.714215,-73.981346,30,502],['Station 503, E 20 St & Park Ave',40.73827428,-73.98751968,5,503],['Station 504, 1 Ave & E 15 St',40.73221853,-73.98165557,45,504],['Station 505, 6 Ave & W 33 St',40.74901271,-73.98848395,36,505],['Station 507, E 25 St & 2 Ave',40.73912601,-73.97973776,47,507],['Station 508, W 46 St & 11 Ave',40.76341379,-73.99667444,24,508],['Station 509, 9 Ave & W 22 St',40.7454973,-74.00197139,36,509],['Station 510, W 51 St & 6 Ave',40.7606597,-73.98042047,51,510],['Station 511, E 14 St & Avenue B',40.72938685,-73.97772429,33,511],['Station 512, W 29 St & 9 Ave',40.7500727,-73.99839279,27,512],['Station 513, W 56 St & 10 Ave',40.768254,-73.988639,27,513],['Station 514, 12 Ave & W 40 St',40.76087502,-74.00277668,53,514],['Station 515, W 43 St & 10 Ave',40.76009437,-73.99461843,35,515],['Station 516, E 47 St & 1 Ave',40.75206862,-73.96784384,39,516],['Station 517, E 41 St & Madison Ave',40.752141,-73.979782,52,517],['Station 518, E 39 St & 2 Ave',40.74780373,-73.9734419,39,518],['Station 519, E 42 St & Vanderbilt Ave',40.752416,-73.97837,61,519],['Station 520, W 52 St & 5 Ave',40.75992262,-73.97648516,39,520],['Station 521, 8 Ave & W 31 St',40.75044999,-73.99481051,67,521],['Station 522, E 51 St & Lexington Ave',40.75714758,-73.97207836,51,522],['Station 523, W 38 St & 8 Ave',40.75466591,-73.99138152,51,523],['Station 524, W 43 St & 6 Ave',40.75527307,-73.98316936,3,524],['Station 525, W 34 St & 11 Ave',40.75594159,-74.0021163,39,525],['Station 526, E 33 St & 5 Ave',40.74765947,-73.98490707,40,526],['Station 527, E 33 St & 1 Ave',40.74315566,-73.97434726,55,527],['Station 528, 2 Ave & E 31 St',40.74290902,-73.97706058,39,528],['Station 529, W 42 St & 8 Ave',40.7575699,-73.99098507,41,529],['Station 530, 11 Ave & W 59 St',40.771522,-73.990541,36,530],['Station 531, Forsyth St & Broome St',40.71893904,-73.99266288,39,531],['Station 532, S 5 Pl & S 4 St',40.710451,-73.960876,43,532],['Station 533, Broadway & W 39 St',40.75299641,-73.98721619,50,533],['Station 534, Water - Whitehall Plaza',40.70255065,-74.0127234,31,534],['Station 536, 1 Ave & E 30 St',40.74144387,-73.97536082,29,536],['Station 537, Lexington Ave & E 24 St',40.74025878,-73.98409214,39,537],['Station 538, W 49 St & 5 Ave',40.75795248,-73.97787642,35,538],['Station 539, Metropolitan Ave & Bedford Ave',40.71534825,-73.96024116,31,539],['Station 540, Lexington Ave & E 26 St',40.74147286,-73.98320928,39,540],['Station 545, E 23 St & 1 Ave',40.736502,-73.97809472,27,545],['Station 546, E 30 St & Park Ave S',40.74444921,-73.98303529,38,546],['Station 2000, Front St & Washington St',40.70255088,-73.98940236,30,2000],['Station 2001, Sands St & Navy St',40.699773,-73.979927,15,2001],['Station 2002, Wythe Ave & Metropolitan Ave',40.716887,-73.963198,27,2002],['Station 2003, 1 Ave & E 18 St',40.73416059,-73.98024289,30,2003],['Station 2004, 6 Ave & Broome St',40.724399,-74.004704,36,2004],['Station 2005, Railroad Ave & Kay Ave',40.70531194,-73.97100056,12,2005],['Station 2006, Central Park S & 6 Ave',40.76590936,-73.97634151,46,2006],['Station 2008, Little West St & 1 Pl',40.70569254,-74.01677685,24,2008],['Station 2009, Catherine St & Monroe St',40.71117444,-73.99682619,35,2009],['Station 2010, Grand St & Greene St',40.72165481,-74.00234737,39,2010],['Station 2012, E 27 St & 1 Ave',40.739445,-73.976806,36,2012],['Station 2017, E 43 St & 2 Ave',40.75022392,-73.97121414,38,2017],['Station 2021, W 45 St & 8 Ave',40.75929124,-73.98859651,43,2021],['Station 2022, E 59 St & Sutton Pl',40.75849116,-73.95920622,33,2022],['Station 2023, E 55 St & Lexington Ave',40.75968085,-73.97031366,36,2023],['Station 3002, South End Ave & Liberty St',40.711512,-74.015756,25,3002]];
	locations = np.array(locations)
	d1=pd.DataFrame(locations);d1.columns=['stationName','latitude','longitude','Docks','id']


	startstationID = int(startStation_input)# 318
	startstationID0 = startstationID
	endstationID0 =  int(endStation_input)# 477
	
	StartYear=int(year_input)
	StartMonth = int(month_input) #7
	StartDay = int(day_input)#3
	StartHour = int(hour_input)#23
	StartMinute = int(minute_input)#58

	ProbTolerance = 0.1 # tolerance of the probability of available bikes/docks when choosing the best station choice
	Tolerance = 4 # tolerance for number of docks
	indStartStationID = pd.Index(d1.id).get_loc(str(startstationID))
	indEndStationID = pd.Index(d1.id).get_loc(str(endstationID0))

	WalkingSpeed = 0.05 # in miles/minute
	MaxNumberOfClosebyStations = 3
	MaxNumberOfClosebyStationsFinal = 3	
	DeltaTimeInMinutes = 15 # for defining neighborhood around time of arrival
	DeltaTimeInSeconds = DeltaTimeInMinutes*60
	DeltaDays =15;
	StartStationsResultsTable = pd.DataFrame(columns=('stationName','distance','traveltime','traveltimemin','traveltimemax','prob','probstring','stationID','isprefered','score'))
	EndStationsResultsTable = pd.DataFrame(columns=('stationName','distance','traveltime','traveltimemin','traveltimemax','prob','probstring','stationID','isprefered','score'))
	## Finding the closest stations to the chosen start station
	DistanceList = numpy.zeros((len(d1), 4 ))
	for i in range((len(d1))):
	    DistanceList[i][0] = distanceLatLon(float(d1.latitude[i]), float(d1.longitude[i]), float(d1.latitude[indStartStationID]), float(d1.longitude[indStartStationID]))
	    DistanceList[i][1] = i
	    DistanceList[i][2] = int(d1.id[i])
	    DistanceList[i][3] = distanceLatLon(float(d1.latitude[i]), float(d1.longitude[i]), float(d1.latitude[indStartStationID]), float(d1.longitude[indStartStationID]))

	DistanceList = pd.DataFrame(DistanceList);DistanceList.columns=['distance','ind','id','StartToEndDistance']
	ClosestStations = DistanceList.sort(['distance'])[0:MaxNumberOfClosebyStations]
	ClosestStations = ClosestStations.reset_index()
	for i in range(len(ClosestStations)):
	    StartStationsResultsTable = StartStationsResultsTable.append(dict(stationName=locations[ClosestStations.ind[i],0],distance=ClosestStations.StartToEndDistance[i],traveltime=0, traveltimemin = 0, traveltimemax=0,  prob=-1, probstring="sorry, no data!",  stationID =  int(ClosestStations.id[i]),isprefered= "", score=0, StartToEndDistance=0   ) , ignore_index=True   )

	## Finding the closest stations to the chosen station of destination
    	StartStationsResultsTable.isprefered[0]="-INITIAL CHOICE";
	DistanceList = numpy.zeros((len(d1), 4 ))
	for i in range((len(d1))):
	    DistanceList[i][0] = distanceLatLon(float(d1.latitude[i]), float(d1.longitude[i]), float(d1.latitude[indEndStationID]), float(d1.longitude[indEndStationID]))
	    DistanceList[i][1] = i
	    DistanceList[i][2] = int(d1.id[i])
	    DistanceList[i][3] = distanceLatLon(float(d1.latitude[i]), float(d1.longitude[i]), float(d1.latitude[indStartStationID]), float(d1.longitude[indStartStationID]))

	DistanceList = pd.DataFrame(DistanceList);DistanceList.columns=['distance','ind','id','StartToEndDistance']
	ClosestStations = DistanceList.sort(['distance'])[0:MaxNumberOfClosebyStations]
	ClosestStations = ClosestStations.reset_index()
	for i in range(len(ClosestStations)):
            EndStationsResultsTable = EndStationsResultsTable.append(dict(stationName=locations[ClosestStations.ind[i],0],distance=ClosestStations.distance[i],traveltime=0, traveltimemin = 0, traveltimemax=0, prob=-1, probstring="sorry, no data!", stationID =  int(ClosestStations.id[i]),isprefered= "", score=0, StartToEndDistance=ClosestStations.StartToEndDistance[i]    ) , ignore_index=True   )

    	EndStationsResultsTable.isprefered[0]="-INITIAL CHOICE";
	###  looping over the 5 start and end stations #######################################################
	###  looping over the probabilities of the closest start stations #######################################################
	for i in range(MaxNumberOfClosebyStations):
		print ([i,len(EndStationsResultsTable)])
		endstationID = int(EndStationsResultsTable.stationID[i])
		startstationID = int(StartStationsResultsTable.stationID[i])
		indStartStationID = pd.Index(d1.id).get_loc(str(startstationID))
		indEndStationID = pd.Index(d1.id).get_loc(str(endstationID))
		EndStationTotalDocks =  int(locations[indEndStationID,3])
		## setting up the start time of departure and the time window around it #######################################################
		StartTime = datetime.datetime(StartYear,StartMonth,StartDay,StartHour,StartMinute,00)
		StartTimeLow = StartTime - datetime.timedelta(0,DeltaTimeInSeconds) # days, seconds, then other fields.
		StartTimeHigh = StartTime + datetime.timedelta(0,DeltaTimeInSeconds) # days, seconds, then other fields.
		StartDateLow = StartTime - datetime.timedelta(days=DeltaDays)
		StartDateHigh = StartTime + datetime.timedelta(days=DeltaDays)
		if ((StartDateLow.month ==6) & (StartDateHigh.month ==6)) | ((StartDateLow.month ==6) & (StartDateHigh.month > StartDateLow.month)): # since we don't have data for June, we use July instead
		   StartDateLow=StartDateLow.replace(month = 7);StartDateLow=StartDateLow.replace(day=1);StartDateHigh = StartDateLow + datetime.timedelta(days=2*DeltaDays)

		if (StartDateHigh.month ==6) & (StartDateHigh.month > StartDateLow.month): #  # since we don't have data for June, we use May instead
		   StartDateHigh.replace(month = 5);StartDateHigh.replace(day=31); StartDateLow = StartDateHigh - datetime.timedelta(days=2*DeltaDays);

		if (StartDateLow.month <=12) & (StartDateLow.month >= 6):
		    StartDateLow=StartDateLow.replace(year =2013)
		else:
		    StartDateLow=StartDateLow.replace(year =2014)

		if (StartDateHigh.month <=12) & (StartDateHigh.month >= 6):
		    StartDateHigh=StartDateHigh.replace(year =2013)
		else:
		    StartDateHigh=StartDateHigh.replace(year =2014)

		##############################################################################
		######  calculating the probability of no bikes available for the start stations
		if StartTimeHigh.hour < StartTimeLow.hour:
		    TimeSelectString =  "  ((TIME(time) between '00:00:00' and '" + str(StartTimeHigh.time()) + "') or (TIME(time) between '" + str(StartTimeLow.time()) + "' and '23:59:59')  ) "
		else:
		    TimeSelectString =  " (TIME(time) between '" + str(StartTimeLow.time()) + "' and '" + str(StartTimeHigh.time()) + "') "

		if (StartTime.weekday() >=5) | is_holiday(str(StartTime.date()))  :
		    DaySelectString  = " (DAYOFWEEK(time)>=6 ) "#  or (time in (select holiday from CityBikes.Holidays as s)) " # weekend or not
		else:
		    DaySelectString  = " (DAYOFWEEK(time)<6 ) "# or (time not in (select holiday from CityBikes.Holidays as s)) "

		DateSelectString = " (time between DATE('"+ str(StartDateLow) + "') and DATE('" + str(StartDateHigh) + "')) "
		#sql2 = "select count(AvailableBikes) as NumDataPoints, sum(case when AvailableBikes<="+	str(Tolerance) +" then 1 else 0 end)/count(AvailableBikes) as probNoAvailBikes from CityBikes.station"+str(startstationID)+"  where " + TimeSelectString + ' and '+ DaySelectString + ' and '+ DateSelectString
		#sql2 = "select avg(probNoAvailBikes) as probNoAvailBikes from ( select count(AvailableBikes) as NumDataPoints, sum(case when AvailableBikes<="+	str(Tolerance) +" then 1 else 0 end)/count(AvailableBikes) as probNoAvailBikes from CityBikes.station"+str(startstationID)+"  where " + TimeSelectString + ' and '+ DaySelectString + ' and '+ DateSelectString + " group by DATE(time) ) as s"
		sql2 = "select sum(probNoAvailBikes/NumDataPoints)/sum(1/NumDataPoints) as probNoAvailBikes from ( select count(AvailableBikes) as NumDataPoints, sum(case when AvailableBikes<="+	str(Tolerance) +" then 1 else 0 end)/count(AvailableBikes) as probNoAvailBikes from CityBikes.station"+str(startstationID)+"  where " + TimeSelectString + ' and '+ DaySelectString + ' and '+ DateSelectString + " group by DATE(time) ) as s"
		print(sql2)
		try:
			probNoAvailBikes = pd.read_sql(sql2, db).probNoAvailBikes[0]
			print(probNoAvailBikes)
			StartStationsResultsTable.prob[i] = 1-probNoAvailBikes
			StartStationsResultsTable.probstring[i] = str(int(100*(1-probNoAvailBikes)))+"%"
		except:
			pass
		
		##############################################################################
		######  calculating the score
		StartStationsResultsTable.score[i] = StartStationsResultsTable.prob[i]/(1+StartStationsResultsTable.distance[i])
		

	############## end forloop
	print("fillresultstable")
	StartStationsResultsTable = StartStationsResultsTable.sort(['score','prob'],ascending=False).reset_index()
    	startstationID0new = int(StartStationsResultsTable.stationID[0])

    	##########################################################################################################################################
	###  looping over the closest end stations and calculate the trip times #######################################################
	for i in range(MaxNumberOfClosebyStations):
		print ([i,len(EndStationsResultsTable)])
		endstationID = int(EndStationsResultsTable.stationID[i])
		startstationID = int(StartStationsResultsTable.stationID[i])
		indStartStationID = pd.Index(d1.id).get_loc(str(startstationID))
		indEndStationID = pd.Index(d1.id).get_loc(str(endstationID))
		EndStationTotalDocks =  int(locations[indEndStationID,3])
		## setting up the start time of departure and the time window around it #######################################################
		StartTime = datetime.datetime(StartYear,StartMonth,StartDay,StartHour,StartMinute,00)
		StartTimeLow = StartTime - datetime.timedelta(0,DeltaTimeInSeconds) # days, seconds, then other fields.
		StartTimeHigh = StartTime + datetime.timedelta(0,DeltaTimeInSeconds) # days, seconds, then other fields.
		StartDateLow = StartTime - datetime.timedelta(days=DeltaDays)
		StartDateHigh = StartTime + datetime.timedelta(days=DeltaDays)
		if ((StartDateLow.month ==6) & (StartDateHigh.month ==6)) | ((StartDateLow.month ==6) & (StartDateHigh.month > StartDateLow.month)): # since we don't have data for June, we use July instead
		   StartDateLow=StartDateLow.replace(month = 7);StartDateLow=StartDateLow.replace(day=1);StartDateHigh = StartDateLow + datetime.timedelta(days=2*DeltaDays)

		if (StartDateHigh.month ==6) & (StartDateHigh.month > StartDateLow.month): #  # since we don't have data for June, we use May instead
		   StartDateHigh.replace(month = 5);StartDateHigh.replace(day=31); StartDateLow = StartDateHigh - datetime.timedelta(days=2*DeltaDays);

		if (StartDateLow.month <=12) & (StartDateLow.month >= 6):
		    StartDateLow=StartDateLow.replace(year =2013)
		else:
		    StartDateLow=StartDateLow.replace(year =2014)

		if (StartDateHigh.month <=12) & (StartDateHigh.month >= 6):
		    StartDateHigh=StartDateHigh.replace(year =2013)
		else:
		    StartDateHigh=StartDateHigh.replace(year =2014)

		######calculating the mean travel time in seconds #######################################################
		if StartTimeHigh.hour < StartTimeLow.hour:
		    TimeSelectString =  "  ((TIME(starttime) between '00:00:00' and '" + str(StartTimeHigh.time()) + "') or (TIME(starttime) between '" + str(StartTimeLow.time()) + "' and '23:59:59')  ) "
		else:
		    TimeSelectString =  " (TIME(starttime) between '" + str(StartTimeLow.time()) + "' and '" + str(StartTimeHigh.time()) + "') "

		if (StartTime.weekday() >=5) | is_holiday(str(StartTime.date())):
			DaySelectString  = " (DAYOFWEEK(starttime)>=6  or starttime in (select holiday from CityBikes.Holidays as s)) " # weekend or not
		else:
			DaySelectString  = " (DAYOFWEEK(starttime)<6  or starttime not in (select holiday from CityBikes.Holidays as s)) "

		DateSelectString = " (starttime between DATE('"+ str(StartDateLow) + "') and DATE('" + str(StartDateHigh) + "')) "
		sql1= 'select tripduration from CityBikes.TripData where startstationid='+str(startstationID0new) +' and endstationid = '+  str(endstationID) + ' and '+ TimeSelectString + ' and '+ DaySelectString + ' and '+ DateSelectString
		rr1 = pd.read_sql(sql1, db)
		if len(rr1) <= 3: # if no trips found, relax constraints
		    sql1= "select tripduration from CityBikes.TripData where startstationid="+str(startstationID0new) +' and endstationid = '+  str(endstationID) + ' and '+ TimeSelectString + ' and '+ DateSelectString
		    rr1 = pd.read_sql(sql1, db)
		    if len(rr1) <= 3: # if no trips found, relax constraints
			sql1= "select tripduration from CityBikes.TripData where startstationid="+str(startstationID0new) +' and endstationid = '+  str(endstationID) + ' and ' + DateSelectString
			rr1 = pd.read_sql(sql1, db)


		if len(rr1)>=1:
			ExpectedTravelTime=np.percentile(rr1.tripduration,50);ExpectedTravelTimeString = str((datetime.timedelta(seconds=int(ExpectedTravelTime) )));
			EndStationsResultsTable.traveltime[i] = str(round(datetime.timedelta(seconds=int(np.percentile(rr1.tripduration,50))).seconds/60.0,1))
			EndStationsResultsTable.traveltimemin[i] = str(round(datetime.timedelta(seconds=int(np.percentile(rr1.tripduration,35))).seconds/60.0,1))
			EndStationsResultsTable.traveltimemax[i] = str(round(datetime.timedelta(seconds=int(np.percentile(rr1.tripduration,65))).seconds/60.0,1))
		else:
		    ExpectedTravelTime=0;ExpectedTravelTimeString = 'sorry, no data!'

		print(ExpectedTravelTimeString)
		##############################################################################
		######  calculating the probabilities for the end stations not having available docks
		dt = datetime.timedelta(seconds=StartHour*3600+StartMinute*60+ ExpectedTravelTime)
		EndTime = datetime.datetime(2014,StartMonth,StartDay,StartHour,StartMinute,00) + datetime.timedelta(days=dt.days,seconds=dt.seconds)
		EndTimeLow = EndTime - datetime.timedelta(0,DeltaTimeInSeconds) # days, seconds, then other fields.
		EndTimeHigh = EndTime + datetime.timedelta(0,DeltaTimeInSeconds) # days, seconds, then other fields.
		EndDateLow = EndTime - datetime.timedelta(days=DeltaDays)
		EndDateHigh = EndTime + datetime.timedelta(days=DeltaDays)
		if ((EndDateLow.month ==6) & (EndDateHigh.month ==6)) | ((EndDateLow.month ==6) & (EndDateHigh.month > EndDateLow.month)): # since we don't have data for June, we use July instead
		   EndDateLow=EndDateLow.replace(month = 7);EndDateLow=EndDateLow.replace(day=1);EndDateHigh = EndDateLow + datetime.timedelta(days=2*DeltaDays)

		if (EndDateHigh.month ==6) & (EndDateHigh.month > EndDateLow.month): #  # since we don't have data for June, we use May instead
		   EndDateHigh.replace(month = 5);EndDateHigh.replace(day=31); EndDateLow = EndDateHigh - datetime.timedelta(days=2*DeltaDays);

		if (EndDateLow.month <=12) & (EndDateLow.month >= 6):
		    EndDateLow=EndDateLow.replace(year =2013)
		else:
		    EndDateLow=EndDateLow.replace(year =2014)

		if (EndDateHigh.month <=12) & (EndDateHigh.month >= 6):
		    EndDateHigh=EndDateHigh.replace(year =2013)
		else:
		    EndDateHigh=EndDateHigh.replace(year =2014)

		######  building the query #######################################################
		if EndTimeHigh.hour < EndTimeLow.hour:
		    TimeSelectString =  "  ((TIME(time) between '00:00:00' and '" + str(EndTimeHigh.time()) + "') or (TIME(starttime) between '" + str(EndTimeLow.time()) + "' and '23:59:59')  ) "
		else:
		    TimeSelectString =  " (TIME(time) between '" + str(EndTimeLow.time()) + "' and '" + str(EndTimeHigh.time()) + "') "

		if (EndTime.weekday() >=5) | is_holiday(str(EndTime.date()))  :
		    DaySelectString  = " (DAYOFWEEK(time)>=6 ) " #  or (time in (select holiday from CityBikes.Holidays as s)) " # weekend or not
		else:
		    DaySelectString  = " (DAYOFWEEK(time)<6 ) " # or (time not in (select holiday from CityBikes.Holidays as s)) "

		DateSelectString = " (time between DATE('"+ str(EndDateLow) + "') and DATE('" + str(EndDateHigh) + "')) "
		sql11 = "select max(AvailableBikes) as MaxAvailableBikes from CityBikes.station"+str(endstationID)+"  where " + DateSelectString
		TotalDockCapacity = pd.read_sql(sql11, db).MaxAvailableBikes[0]
		if TotalDockCapacity == None:
		    TotalDockCapacity = int(locations[indEndStationID][3])

		#sql3 = "select count(AvailableBikes) as NumDataPoints, sum(case when AvailableBikes>="+str(TotalDockCapacity-Tolerance) +" then 1 else 0 end)/count(AvailableBikes) as probNoAvailDocks from CityBikes.station"+str(endstationID)+"  where "+ TimeSelectString + " and " + DaySelectString + " and " + DateSelectString
		#sql3 = "select avg(probNoAvailDocks) as probNoAvailDocks from ( select count(AvailableBikes) as NumDataPoints, sum(case when AvailableBikes>="+str(TotalDockCapacity-Tolerance) +" then 1 else 0 end)/count(AvailableBikes) as probNoAvailDocks from CityBikes.station"+str(endstationID)+"  where "+ TimeSelectString + " and " + DaySelectString + " and " + DateSelectString + " group by DATE(time) ) as s"
		sql3 = "select sum(probNoAvailDocks/NumDataPoints)/sum(1/NumDataPoints) as probNoAvailDocks from ( select count(AvailableBikes) as NumDataPoints, sum(case when AvailableBikes>="+str(TotalDockCapacity-Tolerance) +" then 1 else 0 end)/count(AvailableBikes) as probNoAvailDocks from CityBikes.station"+str(endstationID)+"  where "+ TimeSelectString + " and " + DaySelectString + " and " + DateSelectString + " group by DATE(time) ) as s"
		try:
			probNoAvailDocks = pd.read_sql(sql3, db).probNoAvailDocks[0]
			EndStationsResultsTable.prob[i] = 1-probNoAvailDocks
			EndStationsResultsTable.probstring[i] = str(int(100*(1-probNoAvailDocks)))+"%"
		except:
			pass
		
		##############################################################################
		######  calculating the score
		EndStationsResultsTable.score[i] = EndStationsResultsTable.prob[i]/(1+EndStationsResultsTable.distance[i])
		

	############## end forloop
	print("fillresultstable")
	EndStationsResultsTable = EndStationsResultsTable.sort(['score','prob'],ascending=False).reset_index()
    	ResultsTable=[]
    	for i in range(MaxNumberOfClosebyStationsFinal):
        	ResultsTable.append(dict(stationName=StartStationsResultsTable.stationName[i],distance=StartStationsResultsTable.distance[i],traveltime=StartStationsResultsTable.traveltime[i],traveltimemin=StartStationsResultsTable.traveltimemin[i],traveltimemax=StartStationsResultsTable.traveltimemax[i], probstring=StartStationsResultsTable.probstring[i], prob=StartStationsResultsTable.prob[i], stationID = StartStationsResultsTable.stationID[i],isprefered=StartStationsResultsTable.isprefered[i], StartToEndDistance=0 ) )

    	for i in range(MaxNumberOfClosebyStationsFinal):
    		ResultsTable.append(dict(stationName=EndStationsResultsTable.stationName[i],distance=EndStationsResultsTable.distance[i],traveltime=EndStationsResultsTable.traveltime[i],traveltimemin=EndStationsResultsTable.traveltimemin[i],traveltimemax=EndStationsResultsTable.traveltimemax[i], probstring=EndStationsResultsTable.probstring[i], prob=EndStationsResultsTable.prob[i], stationID = EndStationsResultsTable.stationID[i],isprefered=EndStationsResultsTable.isprefered[i], StartToEndDistance=EndStationsResultsTable.StartToEndDistance[i]) )






	



############################################################################################################################################################


	tmp = '<table id = "ranklist" class="table table-hover">'
	
	tmp = tmp + '<tr style="background-color: yellow;"><th>START STATIONS NEARBY</th> <th> PROBABILITY BIKES AVAILABLE</th><th>EXTRA WALKING TIME</th><th> </th></tr>'

	for i in range(MaxNumberOfClosebyStationsFinal):
		if i==0:
			if ResultsTable[i]["prob"] != None:
				tmp = tmp + '<tr><td><strong>' + str(ResultsTable[i]["stationName"]) +    '</strong> <font color = "blue"> ' + str(ResultsTable[i]["isprefered"]) + '</font>' + '<font color = "red"> - BEST CHOICE!</font>               </td><td>'+ str(ResultsTable[i]["probstring"]) + '</td><td>'+str(round(ResultsTable[i]["distance"]/WalkingSpeed,1))+' min. (' + str(round(ResultsTable[i]["distance"],2))  + ' miles)</td><td> </td></tr>'

		else:	
			if ResultsTable[i]["prob"] != None:
				tmp = tmp + '<tr><td>' + str(ResultsTable[i]["stationName"]) +    '</strong> <font color = "blue"> ' + str(ResultsTable[i]["isprefered"]) + '</font>' + '</td><td>'+ str(ResultsTable[i]["probstring"]) + '</td><td>' +str(round(ResultsTable[i]["distance"]/WalkingSpeed,1))+' min. (' + str(round(ResultsTable[i]["distance"],2))  + ' miles)</td><td> </td></tr>'


	tmp = tmp + '<tr><th> </th><th> </th><th> </th><th> </th></tr>'	
	#tmp = tmp + '<tr style="background-color: yellow;"><th>From Station '+str(int(ResultsTable[0]["stationID"]))+ ' to... </th><th>RIDING TIME</th><th>PROBABILITY DOCKS AVAILABLE</th><th>DISTANCE</th></tr>'
	tmp = tmp + '<tr style="background-color: yellow;"><th>FROM STATION '+str(startstationID0new)+ ' TO... </th><th>PROBABILITY DOCKS AVAILABLE</th><th>TYPICAL RIDING TIMES</th><th>EXTRA WALKING TIME</th></tr>'

	for i in range(MaxNumberOfClosebyStationsFinal,2*MaxNumberOfClosebyStationsFinal,1):
		if i==MaxNumberOfClosebyStationsFinal:
			if ResultsTable[i]["prob"] != None:
				tmp = tmp + '<tr><td><strong>' + str(ResultsTable[i]["stationName"]) + '</strong>  <font color = "blue"> ' + str(ResultsTable[i]["isprefered"]) + '</font>' +  '<font color = "red"> - BEST CHOICE!</font>  </td><td>' + str(ResultsTable[i]["probstring"]) + '</td><td>'+ str(ResultsTable[i]["traveltimemin"]) +" ~ "+ str(ResultsTable[i]["traveltimemax"]) + ' min. ('+ str(round(ResultsTable[i]["StartToEndDistance"],1)) + ' miles)' + ' </td><td>'+ str(round(ResultsTable[i]["distance"]/WalkingSpeed,2))+' min. (' + str(round(ResultsTable[i]["distance"],2))  + ' miles) </td></tr>'

		else:	
			if ResultsTable[i]["prob"] != None:
				tmp = tmp + '<tr><td>' + str(ResultsTable[i]["stationName"]) + '<font color = "blue"> ' + str(ResultsTable[i]["isprefered"]) + '</font>' + '</td><td>' + str(ResultsTable[i]["probstring"]) + '</td><td>'+ str(ResultsTable[i]["traveltimemin"])+" ~ "+ str(ResultsTable[i]["traveltimemax"]) + ' min. ('+ str(round(ResultsTable[i]["StartToEndDistance"],2)) + ' miles)' + '</td><td>'+ str(round(ResultsTable[i]["distance"]/WalkingSpeed,2))+' min. (' + str(round(ResultsTable[i]["distance"],2))  + ' miles) </td></tr>'



		
	tmp = tmp + '</table>'
	
	return tmp






def is_holiday(current_date):
  holiday_list = ['2014-1-1','2014-1-20','2014-2-17','2014-5-26','2014-7-4','2014-9-1','2014-10-13','2014-11-11','2014-11-27','2014-12-25','2015-1-1','2015-1-19','2015-2-16','2015-5-25','2015-7-3','2015-9-7','2015-10-12','2015-11-11','2015-11-26','2015-12-25','2016-1-1','2016-1-18','2016-2-15','2016-5-30','2016-7-4','2016-9-5','2016-10-10','2016-11-11','2016-11-24','2016-12-26'];
  if current_date in holiday_list:
    return 1
  else:
    return 0



def distanceLatLon(lat1, long1, lat2, long2):

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc*3960 #6373.0




