

def parsefile(filename):
    mat_type = None

    obj = {}

    with open(filename, "r") as F:
        for line in F.readlines():
            line = line.rstrip()
            entry = '\t' in line
            if entry:
                [algname, size, time] = line.split('\t')

                if mat_type not in obj: obj[mat_type] = {}
                if size not in obj[mat_type]: obj[mat_type][size] = {}
                assert(mat_type != None)
                obj[mat_type][size][algname] = time
            else: # matrix type
                mat_type = line

    return obj

def tolatextable(obj, algs_p=None):
    ret = ""

    mats = list(obj.keys())
    algs = set()
    sizes = set()

    for x in obj.values():
        sizes |= x.keys()
        for y in x.values():
            algs |= y.keys()

    sizes = list(map(str, sorted(list(map(int, sizes)))))
    if algs_p: algs = algs_p

    for mat in mats:
        ret += f"\n\n Matrix: {mat} \n\n"
        lbreak = "\\hline \n"
        ret +=  "\\begin{tabular}{||"+("c"*(len(algs)+1))+"||} \n" 
        ret += lbreak
        ret += "size & " + " & ".join([k.replace('_', '-') for k in algs]) + "\\\\ [0.5ex] \n"
        ret += lbreak+lbreak

        for size in sizes:
            ret += f"{size} & " + " & ".join([
                "{:.7}s".format(obj[mat][size][a]) if a in obj[mat][size] else "?" 
                for a in algs])
            ret += " \\\\ [1ex] \n"
            ret += lbreak

        ret += "\\end{tabular} \n"

    return ret

def tolatextikzgraph(obj, algs_p=None):
    ret = ""

    mats = list(obj.keys())
    algs = set()
    sizes = set()
    colors = ["red", "blue", "green", "yellow", "purple"]

    for x in obj.values():
        sizes |= x.keys()
        for y in x.values():
            algs |= y.keys()

    sizes = list(map(str, sorted(list(map(int, sizes)))))
    if algs_p: algs = algs_p

    for mat in mats:
        ret += f'''
\\begin{{tikzpicture}}
    \\begin{{axis}}[
        title={{Execution times comparaison for {mat} matrix}},
        xlabel={{size of the matrix}},
        ylabel={{execution time in seconds}},
        legend pos=north west,
        ymajorgrids=true,
        grid style=dashed,
    ]\n\n
        '''

        for alg_i, alg in enumerate(algs):
            ret += f'''
\\addplot[
    color={colors[alg_i]},
    mark=square,
    ]
    coordinates {{{
    "".join([f"({size},{obj[mat][size][alg]})" if alg in obj[mat][size] else "" for size in sizes])
    }}};
    \\addlegendentry{{{alg.replace("_", "-")}}};
    \n
            '''
        ret += '''
\end{axis}
\end{tikzpicture}
        '''

    return ret


if __name__ == "__main__":
    obj = parsefile("./test/perf-combined.txt")
    print(tolatextikzgraph(obj, ["grid", "prediction_correction", "componentwise_grid"]))