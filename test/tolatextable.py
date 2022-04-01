

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

def tolatextable(obj):
    ret = ""

    mats = list(obj.keys())
    algs = set()
    sizes = set()

    for x in obj.values():
        sizes |= x.keys()
        for y in x.values():
            algs |= y.keys()

    sizes = list(map(str, sorted(list(map(int, sizes)))))
    algs = ["grid", "prediction_correction"]

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


if __name__ == "__main__":
    obj = parsefile("./test/perf-combined.txt")
    print(tolatextable(obj))