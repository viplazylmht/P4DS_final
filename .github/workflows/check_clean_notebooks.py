# this template was built from this tutorial: https://github.com/mcullan/jupyter-actions

import argparse
import json

def error_exit(e=None, mess=None):
    # did you know: this func 100% raise error unless you pass nothing to params

    if e:
        print(e)
        raise e

    if mess:
        print(mess)
        raise Exception(mess)

def process_notebook(notebook_filename):
    """
    In this action, we check all metadata, execution_count, id and outputId (gen by google colab) by each cell in notebook
    """
    data = {}

    with open(notebook_filename, encoding="utf8") as f:
        data = json.load(f)

    try:
        for cell in data['cells']:
            cell['metadata'] = {}

            if ('id' in cell['metadata'].keys()):
                error_exit(mess='Contain id in metadata')

            if ('colab' in cell['metadata'].keys()):
                error_exit(mess='Contain colab in metadata')

            if ('outputId' in cell.keys()):
                error_exit(mess='Contain outputId in cell')

            if cell["cell_type"] == 'code':
                if cell['execution_count'] != None:
                    error_exit(mess='execution_count was not set to null')

                if 'outputs' in cell.keys():

                    for o in cell['outputs']:
                        if 'execution_count' in o:
                            if o['execution_count'] != None:
                                error_exit(mess='execution_count (@output) was not set to null')

            elif 'execution_count' in cell.keys():
                error_exit(mess='None code cell contain execution_count')
   
    except Exception as e:
        error_exit(e=e)

    print(f"Processed {notebook_filename}: pass!")

    return

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='read some notebook files')
    parser.add_argument('notebooks',
                        metavar='Notebooks', 
                        type=str, 
                        nargs='+',
                        help='notebooks')

    args = parser.parse_args()

    notebooks = args.notebooks

    for fn in notebooks:
        if not fn.endswith('.ipynb'):
            print(f'Error: file {fn} is not an IPython notebook.')
            raise
        
    for fn in notebooks:
        process_notebook(fn)