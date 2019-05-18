def chooseSpinson():
    return 1


def spinsonAction(i):
    return 1


if __name__ == '__main__':
    no_spinsons = 100
    no_MC = 1000
    no_independent = 100

    for k in range(no_independent):
        for j in range(no_MC):
            for i in range(no_spinsons):
                spinson = chooseSpinson()
                spinsonAction(spinson)


