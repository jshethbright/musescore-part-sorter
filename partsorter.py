import os
import yaml
import argparse

def get_instrument_part(filename):
    return filename\
            .split('.')[0]\
            .split('-')[0]\
            .lower()\
            .strip()\
            .replace(' ', '_')

def load_partmap(partmapfile):
    with open(partmapfile, 'r') as file:
        partmap = yaml.load(file, Loader=yaml.Loader)
        return partmap

def sort_pdfs_to_parts(pdfdir, partmap):
    files = [f for f in os.listdir(pdfdir) if f.endswith('.pdf')]
    partsdir = os.path.join(pdfdir, 'parts')
    if not os.path.exists(partsdir):
        os.mkdir(partsdir)
    
    for part in partmap.keys():
        if not os.path.exists(os.path.join(partsdir, part)):
            os.mkdir(os.path.join(partsdir, part))

    if not os.path.exists(os.path.join(partsdir, 'other')):
        os.mkdir(os.path.join(partsdir, 'other'))
    
    inverse_map = {value: key for key in partmap for value in partmap[key]}
    
    for file in files:
        part = get_instrument_part(file)
        if part in inverse_map.keys():
            outputdir = os.path.join(partsdir, inverse_map[part])
        else:
            outputdir = os.path.join(partsdir, 'other')
        
        os.replace(os.path.join(pdfdir, file), os.path.join(outputdir, file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort PDF files into directories based on their instrument part')
    parser.add_argument('pdfdir', type=str, help='Path to directory containing PDF files')
    parser.add_argument('partmapfile', type=str, help='YAML string mapping instruments to section')
    args = parser.parse_args()

    partmap = load_partmap(args.partmapfile)

    sort_pdfs_to_parts(args.pdfdir, partmap)