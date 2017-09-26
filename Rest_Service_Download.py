# Import Libraries
import arcgis
import io, json, urllib

def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    print (out.replace('/n',''))
    return out

# Open Rest Service
source = input("Input Server URL (with Quotation Marks): ")
service = arcgis.ArcGIS(source)

# Find Layer Names and IDs #TODO Server Type cases (MapServer, FeatureServer, etc)
page = urllib.urlopen(source)
readpage = page.read()

start_index = readpage.index("Layers:")
trim_start = readpage[start_index:]

end_index = trim_start.index("Description:")
trim = trim_start[:end_index]

#Add condition, if "Tables:" is true, delete from there onwards as well, otherwise continue
#print trim

trim_clean = remove_html_markup(trim)
#trim2 = trim1.rstrip('\n')

# Extract Spatial Data

layer_id = input("Layer Id: ")
count = service.get(layer_id, count_only=True)
print ("Downloading", count, "features...")
fields = service.enumerate_layer_fields(layer_id)
print ("Fields: ")
for field in fields:
    print (field)

### add condition of type of extraction: exact ( = ), lower/upper limit (>, >=, <, <=)  or range (x and y)
### and have user input the type of query

### add interactive field mapping, where after user selects layer from service, it displays the fields
### and askes if query by field y/n
    
#limit = input("Limit the number of features to: ")   ###
##helkot
    
shapes = service.get(layer_id) ### Original
### shapes = service.get(layer_id,where="STATUS = '6'",srid='4326') ### get where STATUS (of helkot) is 6
### shapes = service.get(layer_id,where="OBJECTID < '90000'") ### ,where..
### shapes = service.get(layer_id,where="OBJECTID >= '85000' and OBJECTID <= '90000'")
### shapes = service.get(layer_id,where="REGION_ID = 0")  ### to get Helkot by Mahoz, don't forget 0  

### KKL service: "Field ='Value'", MOIN service: "Field = Value"

# Save Output File
outfile = input("Out File Name (with Quotation Marks): ")
###outfile = "helkot_pa"
with io.open(outfile, "w", encoding="utf-8") as f:
  f.write(unicode(json.dumps(shapes, ensure_ascii=False)))
