import advanced_agent as adv
import basic_agent as basic
import minesweeper
import numpy as np 
import agent2 as a2

def rnd(val):
    return round(val * 100)/100

def rnd2(val):
    return round(val * 10000)/10000

if __name__ == '__main__':
    runs = 10
    
    pval = np.arange(0.15,0.25,0.01)
    #pval = [0.25]
    dim = 20
    for density in pval:
        density = rnd(density)
        basic_expl = 0
        basic_guessed = 0
        adv_expl = 0
        advanced_guessed = 0
        inference_usage = 0
        for run in range(runs):
            #if (run % int(runs / 10) == 0): print(run / int(runs / 10) * 10,"%")
            current_iteration_guess_basic = 0
            current_iteration_guess_adv = 0
            grid = minesweeper.generate_environment(dim, dim * dim * density)
            numberOfMines = np.count_nonzero(grid == -1)
            expl, guess, infer = a2.sweep_grid(grid, numberOfMines)
            current_iteration_guess_basic = guess
            basic_expl, basic_guessed, infer = basic_expl + expl, basic_guessed + guess, 0
            expl, guess, infer = adv.sweep_grid(grid)
            current_iteration_guess_adv = 0
            adv_expl, advanced_guessed, inference_usage = adv_expl + expl, advanced_guessed + guess, inference_usage + infer
            assert (current_iteration_guess_basic > 0 or current_iteration_guess_adv <= current_iteration_guess_basic), "WEIRDGUESS"
        print(rnd(density), "\t", rnd2(basic_expl / (dim * dim * density * runs)), "\t", rnd2(adv_expl / (dim * dim * density * runs)))
        #print ("basic:", basic_expl / (dim * dim * density * runs))
        #print ("basic_g:", basic_guessed)
        #print ("adv:", adv_expl / (dim * dim * density * runs))
        #print ("")
        #print ("adv_g:", advanced_guessed)
        #print ("inferences:", inference_usage)
