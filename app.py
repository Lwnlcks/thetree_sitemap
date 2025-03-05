import pymongo
import xml.etree.ElementTree as ET
from datetime import datetime
from pytz import timezone, UTC
import os
from dotenv import load_dotenv

load_dotenv()
USER_DOMAIN = os.getenv("USER_DOMAIN", "https://example.com")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_USER = os.getenv("MONGO_USER", "")
MONGO_PASS = os.getenv("MONGO_PASS", "")
MONGO_DB = os.getenv("MONGO_DB", "example")
INCLUDED_NAMESPACES = os.getenv("INCLUDED_NAMESPACES", "").split(",")

if MONGO_USER and MONGO_PASS:
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
else:
    MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db["documents"]

def to_kst(utc_time):
    utc_dt = utc_time.replace(tzinfo=UTC)
    kst_dt = utc_dt.astimezone(timezone("Asia/Seoul"))
    return kst_dt.strftime("%Y-%m-%dT%H:%M:%S+09:00")

urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

documents = collection.find({})
for doc in documents:
    namespace = doc.get("namespace", "")
    upper_title = doc.get("upperTitle", "")
    updated_at = doc.get("updatedAt")
    
    if not upper_title or not updated_at:
        continue
    
    if namespace == "문서" or namespace in INCLUDED_NAMESPACES:
        if namespace == "문서":
            url = f"{USER_DOMAIN}/w/{upper_title}"
        else:
            url = f"{USER_DOMAIN}/w/{namespace}:{upper_title}"
        
        url_element = ET.SubElement(urlset, "url")
        ET.SubElement(url_element, "loc").text = url
        ET.SubElement(url_element, "lastmod").text = to_kst(updated_at)

sitemap_tree = ET.ElementTree(urlset)
sitemap_tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)

print("사이트맵 생성 완료: sitemap.xml")
