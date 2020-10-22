import bs4
import requests
from pathlib import Path

def getpsets(url, outdir):
    """copy IFC PSD-XMLs to local storage"""
    r = requests.get(url)
    data = bs4.BeautifulSoup(r.text, "html.parser")
    for l in data.find_all("a"):
        pset = l["href"]
        if not pset.startswith("Pset"): continue;
        r = requests.get(url + pset)
        print("{} ({})".format(pset, r.status_code))

        with open((outdir / pset).resolve(), "w", encoding="utf-8") as f:
             f.write(r.content.decode('utf-8'))
        





if __name__ == "__main__":
    source = "https://standards.buildingsmart.org/IFC/DEV/IFC4_2/FINAL/HTML/psd/"
    target = (Path(__file__).parent / 'psets' / 'xml')
    getpsets(source, target)