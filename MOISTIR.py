import psycopg2, os, time
import time

start = time.time()
print start

isles = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
index = 0

years = raw_input("Enter a number of years to predict begining from 2010: ")
y = int(years)
period = raw_input("Enter regression period of 1850, 1925 or 1970: ")
p = int(period)

for isle, index in enumerate(isles):
        conn = psycopg2.connect(dbname = 'xxx', host= 'localhost', port= 5432, user = 'postgres',password= 'xxxxxx')
        conn.autocommit = True
        cur = conn.cursor()  ## open a cursor
        
        thesql = """DROP table bobo;
        DROP table bobo2;
        DROP table bobo3;
        SELECT i.transorder as iid, st_x(st_centroid(i.geom)) as X0, st_y(st_centroid(i.geom)) as Y0, t.transorder as tid, t.azimuth as az, r.tid as rid, r."%s" as reg
        INTO bobo
        FROM intersect%s as i, trans%sutm as t, r%s as r
        WHERE i.transorder = t.transorder and i.transorder = r.tid;

        SELECT *, (((b.reg * %s) * (sin(radians(b.az)))+ b.x0)) as x2, (((b.reg * %s) * (cos(radians(b.az)))+ b.y0)) as y2
        INTO bobo2
        FROM bobo as b;

        SELECT *, st_setsrid(st_makepoint(b.x2,b.y2),26918) as geom
        INTO newShore_points%s
        from bobo2 as b;

        SELECT iid, st_makeline(ARRAY(SELECT st_centroid(b.geom) FROM newShore_points%s as b ORDER BY b.iid)) as geom
        INTO bobo3
        FROM newShore_points%s as b
        GROUP BY b.iid;

        SELECT iid, st_setsrid(b.geom, 26918)
        INTO newShore_line%s
        FROM bobo3 as b; """
        
        print thesql
        i = isle
        print isle, index
        index += 1
        cur.execute(thesql,(p,i+1,i+1,i+1,y,y,i+1,i+1,i+1,i+1,))
        cur.close()
        conn.close()

        
end = time.time()
print end - start

